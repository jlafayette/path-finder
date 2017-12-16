import pygame

import breadth_first
from grid import Grid


SCREEN_SIZE = (800, 800)


class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class Shared(Borg):
    def __init__(self, initialize=False):
        Borg.__init__(self)
        if initialize:
            self.screen = pygame.display.set_mode(SCREEN_SIZE)
            self.clock = pygame.time.Clock()
            self.grid = Grid(self.screen, 40, 40, 16, SCREEN_SIZE)
            self.generator = None
            self.state = CreateState()


class BaseState(object):
    def __init__(self):
        self.fps = 60

    def handleinput(self):
        for event in pygame.event.get():
            self.process_event(event)

    def process_event(self, event):
        if event.type == pygame.QUIT:
            raise RuntimeError

    def update(self):
        pass

    def draw(self):
        pass


class CreateState(BaseState):
    def __init__(self):
        super(CreateState, self).__init__()
        Shared().generator = None

    def handleinput(self):
        super(CreateState, self).handleinput()

    def process_event(self, event):
        super(CreateState, self).process_event(event)

    def update(self):
        Shared().grid.refresh()

    def draw(self):
        Shared().grid.draw()
        pygame.display.update()
        Shared().state = IdleState()


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

        # add key press event for STEP_SOLVE


class SolveState(BaseState):
    def __init__(self):
        super(SolveState, self).__init__()
        self.fps = 240
        shared = Shared()
        if shared.generator is None:
            shared.generator = breadth_first.search(shared.grid)

        self.goal_block = None
        self.updated_blocks = list()

    def handleinput(self):
        super(SolveState, self).handleinput()

    def process_event(self, event):
        super(SolveState, self).process_event(event)
        shared = Shared()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            shared.state = IdleState()
        # add toggle to step

    def update(self):
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
        for block in self.updated_blocks:
            block.draw(Shared().screen)
        pygame.display.update([block.rect for block in self.updated_blocks])


class SolutionState(BaseState):
    def __init__(self, goal_block):
        super(SolutionState, self).__init__()
        self.block = goal_block

    def update(self):
        if self.block is None:
            Shared().state = DisplayResultState()
        else:
            self.block.solve = True

    def draw(self):
        if self.block is None:
            pass
        else:
            self.block.draw(Shared().screen)
            pygame.display.update([self.block.rect])
            self.block = self.block.parent


class DisplayResultState(BaseState):
    def __init__(self):
        super(DisplayResultState, self).__init__()
        self.fps = 10

    def process_event(self, event):
        super(DisplayResultState, self).process_event(event)
        shared = Shared()
        if event.type == pygame.KEYDOWN:   # press any key to continue
            shared.state = CreateState()


def main():
    pygame.init()
    shared = Shared(initialize=True)
    loop = 0
    while True:
        loop += 1
        # print(loop)
        try:
            shared.state.handleinput()
        except RuntimeError:
            break
        else:
            shared.state.update()
            shared.state.draw()
        shared.clock.tick(shared.state.fps)

    # while not done:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             done = True
    #         elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
    #             refresh = True
    #         elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
    #             refresh = True
    #             step_mode = True
    #
    #     # pressed = pygame.key.get_pressed()
    #     # if pressed[pygame.K_UP]:
    #     #     y -= 3
    #     # if pressed[pygame.K_DOWN]:
    #     #     y += 3
    #     # if pressed[pygame.K_LEFT]:
    #     #     x -= 3
    #     # if pressed[pygame.K_RIGHT]:
    #     #     x += 3
    #     screen.fill(color.BLACK)
    #     if refresh:
    #         grid.refresh()
    #         refresh = False
    #         # for result in grid.draw_step():
    #         #     pygame.display.update()
    #         #     clock.tick(480*4)
    #         grid.draw()
    #     else:
    #         grid.draw()
    #
    #     pygame.display.update()
    #     clock.tick(60)
    #
    #     if step_mode:
    #         step_mode = False
    #
    #         zoom = False
    #
    #         goal_block = None
    #         steps = 0
    #         search_generator = breadth_first.search(grid)
    #         while True:
    #             if zoom:
    #                 go_to_next = True
    #             else:
    #                 go_to_next = False
    #             try:
    #                 for event in pygame.event.get():
    #                     if event.type == pygame.QUIT:
    #                         raise UserWarning("DONE!!")
    #                     elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
    #                         go_to_next = True
    #                     elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
    #                         zoom = True
    #             except UserWarning:
    #                 break
    #
    #             if go_to_next:
    #                 try:
    #                     blocks = next(search_generator)
    #                 except StopIteration:
    #                     break
    #                 if blocks[-1].end:
    #                     goal_block = blocks[-1]
    #                 steps += 1
    #
    #                 # add code here to draw and step
    #                 for block in blocks:
    #                     block.draw(screen)
    #                 pygame.display.update([block.rect for block in blocks])
    #
    #                 clock.tick(60*10)
    #
    #         print("steps: {}".format(steps))
    #
    #         print("goal_block: {!r}".format(goal_block))
    #         if goal_block is not None:
    #             for block in breadth_first.construct_path(goal_block):
    #                 try:
    #                     block.solve = True
    #                     block.draw(screen)
    #                 except (TypeError, AttributeError) as exc:
    #                     print("caught err: {}".format(exc))
    #                     pass
    #                 pygame.display.update()
    #                 clock.tick(60*4)


if __name__ == '__main__':
    main()
