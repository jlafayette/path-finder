import random
from collections import namedtuple

import pygame

import color
from block import Block


Position = namedtuple('Position', 'x y')


class Grid(object):
    def __init__(self, screen, preset):

        self.screen = screen
        self.num_x = preset.x_num
        self.num_y = preset.y_num
        self.width = preset.x_num * preset.block_size
        self.height = preset.y_num * preset.block_size
        self.block_size = preset.block_size
        self.allow_diagonal_neighbors = preset.allow_diagonals
        self.wall_percentage = preset.wall_percentage

        remaining_w = preset.screen_size[0] - self.width
        remaining_h = preset.screen_size[1] - self.height
        self.x_pos = int(remaining_w / 2)
        self.y_pos = int(remaining_h / 2)

        self.blocks = []
        for x in range(preset.x_num):
            col = []
            for y in range(preset.y_num):
                col.append(Block(x, y, self.x_pos, self.y_pos, self.block_size, False))
            self.blocks.append(col)

        self.refresh()

    def get_random_position(self, exclude=None):
        x = random.randint(0, self.num_x-1)
        if exclude is not None:
            while x == exclude.x:
                x = random.randint(0, self.num_x-1)
        y = random.randint(0, self.num_y-1)
        if exclude is not None:
            while y == exclude.y:
                y = random.randint(0, self.num_y-1)
        return Position(x, y)

    def set_start_end(self):
        start_pos = self.get_random_position()
        end_pos = self.get_random_position(exclude=start_pos)
        self.blocks[start_pos.x][start_pos.y].start = True
        self.blocks[end_pos.x][end_pos.y].end = True

        # self.blocks[0][int((self.num_y - 1) / 2)].start = True
        # self.blocks[self.num_x - 1][int((self.num_y - 1) / 2)].end = True

    def draw(self):
        pygame.draw.rect(self.screen, color.BLUE,
                         pygame.Rect(self.x_pos, self.y_pos, self.width, self.height))
        for block in self.iter_blocks():
            block.draw(self.screen)

    def draw_step(self):
        pygame.draw.rect(self.screen, color.BLUE,
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
            block.wall = rand_wall(self.wall_percentage)
        self.set_start_end()

    def get_start_block(self):
        for block in self.iter_blocks():
            if block.start:
                return block
        else:
            self.blocks[0][0].start = True
            return self.blocks[0][0]

    def get_end_block(self):
        for block in self.iter_blocks():
            if block.end:
                return block
        else:
            self.blocks[self.num_x-1][self.num_y-1].end = True
            return self.blocks[self.num_x-1][self.num_y-1]

    @staticmethod
    def is_goal(block):
        return block.end

    def get_neighbors(self, block):
        if self.allow_diagonal_neighbors:
            neighbor_coordinates = [
                (block.x - 1, block.y),      # left
                (block.x - 1, block.y + 1),  # top-left
                (block.x, block.y + 1),      # top
                (block.x + 1, block.y + 1),  # top-right
                (block.x + 1, block.y),      # right
                (block.x + 1, block.y - 1),  # bottom-right
                (block.x, block.y - 1),      # bottom
                (block.x - 1, block.y - 1)   # bottom-left
            ]
        else:
            neighbor_coordinates = [
                (block.x - 1, block.y),  # left
                (block.x, block.y + 1),  # top
                (block.x + 1, block.y),  # right
                (block.x, block.y - 1)   # bottom
            ]
        for x, y in neighbor_coordinates:
            if x < 0 or y < 0:   # remove negatives so it doesn't continue across edges
                continue
            try:
                candidate = self.blocks[x][y]
            except IndexError:
                pass
            else:
                if not candidate.wall:
                    yield candidate


def rand_wall(wall_percentage):
    return random.random() < wall_percentage / 100
