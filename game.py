import random

import pygame

import breadth_first


SIZE = (800, 600)
WALL_PERCENTAGE = 20

BLUE = (0, 128, 255)
ORANGE = (255, 100, 0)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)


def tint(color, amount=50):
    return min(color[0]+amount, 255), min(color[1]+amount, 255), min(color[2]+amount, 255)


def shade(color, amount=50):
    return max(color[0]-amount, 0), max(color[1]-amount, 0), max(color[2]-amount, 0)


BLUE_TINT = tint(BLUE)
BLUE_SHADE = shade(BLUE)
YELLOW_SHADE = shade(YELLOW)

WALL_TYPE = "wall"
START_TYPE = "start"
END_TYPE = "end"
NORMAL_TYPE = "normal"
SOLVE_TYPE = "solve"
BLOCK_TYPES = (WALL_TYPE, START_TYPE, END_TYPE, NORMAL_TYPE, SOLVE_TYPE)


def rand_wall():
    return random.random() < WALL_PERCENTAGE / 100


class Block(object):

    def __init__(self, x, y, x_pos_offset, y_pos_offset, size, type_=None):
        self.x = x
        self.y = y
        self.x_pos = x*size + x_pos_offset
        self.y_pos = y*size + y_pos_offset
        self.size = size
        self._type = NORMAL_TYPE
        if type_ is not None:
            self._type = type_

    def draw(self, screen):
        pygame.draw.rect(screen, self.fill_color,
                         pygame.Rect(self.x_pos, self.y_pos, self.size, self.size))
        pygame.draw.rect(screen, self.outline_color,
                         pygame.Rect(self.x_pos, self.y_pos, self.size, self.size), 1)

    @property
    def type_(self):
        return self._type

    @type_.setter
    def type_(self, value):
        if value in BLOCK_TYPES:
            self._type = value
        else:
            raise ValueError("Invalid block type: {}".format(value))

    @property
    def fill_color(self):
        if self.type_ == WALL_TYPE:
            return BLACK
        elif self.type_ in [START_TYPE, END_TYPE]:
            return YELLOW
        elif self.type_ == SOLVE_TYPE:
            return ORANGE
        else:
            return BLUE

    @property
    def outline_color(self):
        if self.type_ == WALL_TYPE:
            return BLACK
        elif self.type_ in [START_TYPE, END_TYPE]:
            return YELLOW_SHADE
        elif self.type_ == SOLVE_TYPE:
            return YELLOW
        else:
            return BLUE_SHADE

    def __repr__(self):
        return "{0.__class__}[{0.x}][{0.y}] type: {0.type_}".format(self)

    def __str__(self):
        return "{!s},{!s}".format(self.x, self.y)


class Grid(object):
    def __init__(self, screen, num_x, num_y, block_size):
        self.screen = screen
        self.num_x = num_x
        self.num_y = num_y
        self.width = num_x * block_size
        self.height = num_y * block_size
        self.block_size = block_size

        remaining_w = SIZE[0] - self.width
        remaining_h = SIZE[1] - self.height
        self.x_pos = int(remaining_w / 2)
        self.y_pos = int(remaining_h / 2)

        self.blocks = []
        for x in range(num_x):
            col = []
            for y in range(num_y):
                if rand_wall():
                    type_ = WALL_TYPE
                else:
                    type_ = NORMAL_TYPE
                col.append(Block(x, y, self.x_pos, self.y_pos, self.block_size, type_))
            self.blocks.append(col)

        # hardcoded for now
        self.blocks[0][int((num_y-1)/2)].type_ = START_TYPE
        self.blocks[num_x-1][int((num_y-1)/2)].type_ = END_TYPE

    def draw(self):
        pygame.draw.rect(self.screen, BLUE,
                         pygame.Rect(self.x_pos, self.y_pos, self.width, self.height))
        for block in self.iter_blocks():
            block.draw(self.screen)

    def draw_step(self):
        pygame.draw.rect(self.screen, BLUE,
                         pygame.Rect(self.x_pos, self.y_pos, self.width, self.height))
        yield
        for block in self.iter_blocks():
            block.draw(self.screen)
            yield

    def iter_blocks(self):
        for i in range(self.num_x):
            for j in range(self.num_y):
                yield self.blocks[i][j]

    def refresh(self):
        for block in self.iter_blocks():
            if block.type_ in [START_TYPE, END_TYPE]:
                pass
            elif rand_wall():
                block.type_ = WALL_TYPE
            else:
                block.type_ = NORMAL_TYPE

    def get_start_block(self):
        for block in self.iter_blocks():
            if block.type_ == START_TYPE:
                return block
        else:
            self.blocks[0][0].type_ = START_TYPE
            return self.blocks[0][0]

    @staticmethod
    def is_goal(block):
        return block.type_ == END_TYPE

    def get_successors(self, block):
        # print(str(block))
        successors = []
        for x, y in [(block.x-1, block.y),   # left
                     (block.x, block.y+1),   # top
                     (block.x+1, block.y),   # right
                     (block.x, block.y-1)    # bottom
                     ]:
            # print("x: {} y: {}".format(x, y))

            if x < 0 or y < 0:   # remove negatives so it doesn't continue across edges
                continue
            try:
                candidate = self.blocks[x][y]
            except IndexError:
                pass
            else:
                if candidate.type_ in [NORMAL_TYPE, END_TYPE]:
                    successors.append(candidate)
        # print("{!s} -> {!s}".format(block, [str(b) for b in successors]))
        return successors


def main():
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    done = False
    refresh = False
    # x = 30
    # y = 30
    grid = Grid(screen, 40, 30, 16)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                refresh = True

        # pressed = pygame.key.get_pressed()
        # if pressed[pygame.K_UP]:
        #     y -= 3
        # if pressed[pygame.K_DOWN]:
        #     y += 3
        # if pressed[pygame.K_LEFT]:
        #     x -= 3
        # if pressed[pygame.K_RIGHT]:
        #     x += 3
        screen.fill(BLACK)
        if refresh:
            grid.refresh()
            refresh = False
            for result in grid.draw_step():
                pygame.display.flip()
                clock.tick(480*4)

            solve = breadth_first.breadth_first_search(grid)
            print(solve)
            print(type(solve))
            if solve is not None:
                for block in solve:
                    try:
                        block.type_ = SOLVE_TYPE
                        block.draw(screen)
                    except (TypeError, AttributeError):
                        pass
                    pygame.display.flip()
                    clock.tick(240)
        else:
            grid.draw()

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
