import sys

import pygame

import color


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
        self.fscore = sys.maxsize
        self.gscore = sys.maxsize

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
        self.fscore = sys.maxsize
        self.gscore = sys.maxsize

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
            return color.BLACK, color.BLACK
        elif self.start or self.end:
            return color.YELLOW, color.YELLOW_SHADE
        elif self.solve:
            return color.GREEN, color.GREEN_SHADE
        elif self.visited:
            return color.GREY, color.GREY_SHADE
        elif self.open:
            return color.YELLOW, color.YELLOW_SHADE
        else:
            return color.BLUE, color.BLUE_SHADE

    def __lt__(self, other):
        return self.fscore < other.fscore

    def __repr__(self):
        return "{0.__class__}[{0.x}][{0.y}] wall: {0.wall}".format(self)

    def __str__(self):
        return "{!s},{!s}".format(self.x, self.y)
