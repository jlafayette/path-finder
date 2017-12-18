import pygame

import breadth_first
import a_star
import color
from grid import Grid


class StandardPreset(object):
    speed_mult = 1
    x_num = 40
    y_num = 30
    block_size = 16
    buffer = 50
    allow_diagonals = True
    wall_percentage = 25

    @property
    def screen_size(self):
        return self.x_num*self.block_size + self.buffer, self.y_num*self.block_size + self.buffer


class LargePreset(StandardPreset):
    speed_mult = 3
    x_num = 350
    y_num = 174
    block_size = 5
    buffer = 50
    allow_diagonals = True
    wall_percentage = 55


class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class Shared(Borg):
    def __init__(self, initialize=False, preset=None):
        Borg.__init__(self)
        if initialize:
            self.screen = pygame.display.set_mode(preset.screen_size)
            self.preset = preset
            self.clock = pygame.time.Clock()
            self.grid = Grid(self.screen, preset)
            self.generator = None
            self.state = CreateState()
            self.search = a_star.search


SEARCH_DICT = {
    pygame.K_b: breadth_first.search,
    pygame.K_a: a_star.search
}


class StatusDisplay(object):

    def __init__(self, x_pos, y_pos):
        self.font = pygame.font.SysFont('input', 16)
        self.x = x_pos
        self.y = y_pos
        try:
            self._text = "Mode: {!s}".format(Shared().state)
        except AttributeError:
            self._text = "Mode: INITIALIZING..."
        self.new_text = True

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self.new_text = True
        self._text = value

    def update(self):
        self.text = "Mode: {!s}".format(Shared().state)

    def draw(self):
        if self.new_text:
            self.new_text = False
            textsurface = self.font.render(self.text, True, color.WHITE, color.BLACK)
            shared = Shared()
            rect = pygame.Rect(self.x, self.y,
                               shared.screen.get_width(), int(shared.preset.buffer/2))
            pygame.draw.rect(shared.screen, color.BLACK, rect)
            shared.screen.blit(textsurface, (self.x, self.y))   # returns pygame.Rect
            pygame.display.update([rect])


class BaseState(object):
    def __init__(self):
        self.fps = 60

    def handleinput(self):
        for event in pygame.event.get():
            self.process_event(event)

    def process_event(self, event):
        if event.type == pygame.QUIT:
            raise RuntimeError
        if event.type == pygame.KEYDOWN:
            try:
                Shared().search = SEARCH_DICT[event.key]
            except KeyError:
                pass

    def update(self):
        pass

    def draw(self):
        pass

    def __str__(self):
        return "BASE"


class CreateState(BaseState):
    def __init__(self):
        super(CreateState, self).__init__()
        Shared().generator = None

    def handleinput(self):
        super(CreateState, self).handleinput()

    def process_event(self, event):
        super(CreateState, self).process_event(event)

    def update(self):
        super(CreateState, self).update()
        Shared().grid.refresh()

    def draw(self):
        super(CreateState, self).draw()
        Shared().grid.draw()
        pygame.display.update()
        Shared().state = IdleState()

    def __str__(self):
        return "CREATE"


class IdleState(BaseState):
    def __init__(self):
        super(IdleState, self).__init__()
        self.fps = 10

    def process_event(self, event):
        super(IdleState, self).process_event(event)
        shared = Shared()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            shared.state = CreateState()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            shared.state = SolveState()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            shared.state = StepSolveState()

    def __str__(self):
        return "IDLE"


class BaseSolveState(BaseState):
    def __init__(self):
        super(BaseSolveState, self).__init__()
        shared = Shared()
        if shared.generator is None:
            shared.generator = shared.search(shared.grid)
        self.goal_block = None
        self.updated_blocks = list()
        self.toggle_state = NotImplemented   # type: BaseState()
        self.toggle_keys = [pygame.K_SPACE]

    def process_event(self, event):
        super(BaseSolveState, self).process_event(event)
        shared = Shared()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            shared.state = CreateState()
        elif event.type == pygame.KEYDOWN and event.key in self.toggle_keys:
            shared.state = self.toggle_state()

    def update(self):
        super(BaseSolveState, self).update()
        shared = Shared()
        try:
            self.updated_blocks = next(shared.generator)
        except StopIteration:
            shared.generator = None
            self.updated_blocks = []
            if self.goal_block is None:
                shared.state = DisplayResultState()
            else:
                shared.state = SolutionState(self.goal_block)
        else:
            if self.updated_blocks[-1].end:
                self.goal_block = self.updated_blocks[-1]

    def draw(self):
        super(BaseSolveState, self).draw()
        for block in self.updated_blocks:
            block.draw(Shared().screen)
        pygame.display.update([block.rect for block in self.updated_blocks])

    def __str__(self):
        return "BASE-SOLVE"


class SolveState(BaseSolveState):
    def __init__(self):
        super(SolveState, self).__init__()
        self.fps = 120
        self.toggle_state = StepSolveState
        self.toggle_keys = [pygame.K_SPACE, pygame.K_RIGHT]

    def __str__(self):
        return "SOLVE"


class StepSolveState(BaseSolveState):
    def __init__(self):
        super(StepSolveState, self).__init__()
        self.fps = 10
        self.toggle_state = SolveState
        self.step = False

    def process_event(self, event):
        super(StepSolveState, self).process_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.step = True

    def update(self):
        if self.step:
            self.step = False
            super(StepSolveState, self).update()
        else:
            # TODO: Add blinking for current block when idle
            pass

    def __str__(self):
        return "STEP-SOLVE"


class SolutionState(BaseState):
    def __init__(self, goal_block):
        super(SolutionState, self).__init__()
        self.block = goal_block

    def update(self):
        super(SolutionState, self).update()
        if self.block is None:
            Shared().state = DisplayResultState()
        else:
            self.block.solve = True

    def draw(self):
        super(SolutionState, self).draw()
        if self.block is None:
            pass
        else:
            self.block.draw(Shared().screen)
            pygame.display.update([self.block.rect])
            self.block = self.block.parent

    def __str__(self):
        return "SOLUTION"


class DisplayResultState(BaseState):
    def __init__(self):
        super(DisplayResultState, self).__init__()
        self.fps = 10

    def process_event(self, event):
        super(DisplayResultState, self).process_event(event)
        shared = Shared()
        if event.type == pygame.KEYDOWN:   # press any key to continue
            shared.state = CreateState()

    def __str__(self):
        return "DISPLAY-RESULT"


def main():
    pygame.init()
    pygame.font.init()
    preset = StandardPreset()
    shared = Shared(initialize=True, preset=preset)
    display = StatusDisplay(0, 0)

    # print("screentype: {}".format(type(shared.screen)))

    loop = 0
    while True:
        loop += 1
        # print("loop: {}".format(loop))
        try:
            shared.state.handleinput()
        except RuntimeError:
            break
        else:
            shared.state.update()
            display.update()
            shared.state.draw()
            display.draw()
        shared.clock.tick(shared.state.fps * preset.speed_mult)


if __name__ == '__main__':
    main()
