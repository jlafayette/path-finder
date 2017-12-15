import random

import pygame

import breadth_first


SIZE = (800, 800)
WALL_PERCENTAGE = 20

BLUE = (0, 128, 255)
ORANGE = (255, 100, 0)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)


def tint(color, amount=50):
    return min(color[0]+amount, 255), min(color[1]+amount, 255), min(color[2]+amount, 255)


def shade(color, amount=50):
    return max(color[0]-amount, 0), max(color[1]-amount, 0), max(color[2]-amount, 0)


BLUE_TINT = tint(BLUE)
BLUE_SHADE = shade(BLUE)
YELLOW_SHADE = shade(YELLOW)
RED_SHADE = shade(RED)
GREEN_SHADE = shade(GREEN)
GREY_SHADE = shade(GREY)


def rand_wall():
    return random.random() < WALL_PERCENTAGE / 100


class Block(object):

    def __init__(self, x, y, x_pos_offset, y_pos_offset, size, wall):
        self.x = x
        self.y = y
        self.x_pos = x*size + x_pos_offset
        self.y_pos = y*size + y_pos_offset
        self.size = size
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.size, self.size)

        self.wall = wall
        self._start = False
        self._end = False
        self.solve = False

        # path-finding attrs
        self.parent = None
        self.open = False
        self.visited = False

    def draw(self, screen):
        fill_color, outline_color = self.colors
        pygame.draw.rect(screen, fill_color, self.rect)
        pygame.draw.rect(screen, outline_color, self.rect, 1)

    def reset(self):
        self.wall = False
        self._start = False
        self._end = False
        self.solve = False
        self.parent = None
        self.open = False
        self.visited = False

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        if value:
            self.wall = False
        self._start = value

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        if value:
            self.wall = False
        self._end = value

    @property
    def colors(self):
        if self.wall:
            return BLACK, BLACK
        elif self.start or self.end:
            return YELLOW, YELLOW_SHADE
        elif self.solve:
            return GREEN, GREEN_SHADE
        elif self.visited:
            return GREY, GREY_SHADE
        elif self.open:
            return YELLOW, YELLOW_SHADE
        else:
            return BLUE, BLUE_SHADE

    def __repr__(self):
        return "{0.__class__}[{0.x}][{0.y}] wall: {0.wall}".format(self)

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
                col.append(Block(x, y, self.x_pos, self.y_pos, self.block_size, rand_wall()))
            self.blocks.append(col)

        self.set_start_end()

    def set_start_end(self):
        self.blocks[0][0].start = True
        self.blocks[self.num_x-1][self.num_y-1].end = True

        # self.blocks[0][int((self.num_y - 1) / 2)].start = True
        # self.blocks[self.num_x - 1][int((self.num_y - 1) / 2)].end = True

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
            block.reset()
            block.wall = rand_wall()
        self.set_start_end()

    def get_start_block(self):
        for block in self.iter_blocks():
            if block.start:
                return block
        else:
            self.blocks[0][0].start = True
            return self.blocks[0][0]

    @staticmethod
    def is_goal(block):
        return block.end

    def get_successors(self, block):
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
                if not candidate.wall:
                    yield candidate


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    done = False
    refresh = False
    step_mode = False
    # x = 30
    # y = 30
    grid = Grid(screen, 40, 40, 16)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                refresh = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                refresh = True
                step_mode = True

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
            # for result in grid.draw_step():
            #     pygame.display.update()
            #     clock.tick(480*4)
            grid.draw()
        else:
            grid.draw()

        pygame.display.update()
        clock.tick(60)

        if step_mode:
            step_mode = False

            zoom = False

            goal_block = None
            steps = 0
            search_generator = breadth_first.search(grid)
            while True:
                if zoom:
                    go_to_next = True
                else:
                    go_to_next = False
                try:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            raise UserWarning("DONE!!")
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                            go_to_next = True
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                            zoom = True
                except UserWarning:
                    break

                if go_to_next:
                    try:
                        blocks = next(search_generator)
                    except StopIteration:
                        break
                    if blocks[-1].end:
                        goal_block = blocks[-1]
                    steps += 1

                    # add code here to draw and step
                    for block in blocks:
                        block.draw(screen)
                    pygame.display.update([block.rect for block in blocks])

                    clock.tick(60*10)

            print("steps: {}".format(steps))

            print("goal_block: {!r}".format(goal_block))
            if goal_block is not None:
                for block in breadth_first.construct_path(goal_block):
                    try:
                        block.solve = True
                        block.draw(screen)
                    except (TypeError, AttributeError) as exc:
                        print("caught err: {}".format(exc))
                        pass
                    pygame.display.update()
                    clock.tick(60*4)


if __name__ == '__main__':
    main()
