import time
import turtle
import random

import click


@click.command()
def test():
    print("starting")

    # screen = turtle.Screen()
    # screen.tracer(0, 0)
    x = 20
    y = 40
    g = Grid(x, y, size=10)

    for i in range(int(x*y/10)):
        g.color_cell(random.randint(0, x-1), random.randint(0, y-1), "red", "yellow")

    # t = turtle.Turtle()
    # t.hideturtle()
    # t.speed(0)
    # t.color('black', 'black')

    # screen.update()
    turtle.done()


class Grid(object):
    def __init__(self, x, y, size=10):
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.speed(0)
        self.screen = turtle.Screen()
        self.screen.bgcolor("grey")
        self.screen.tracer(0, 0)
        self.x = x
        self.y = y
        self._size = size
        self.delay = 0.005
        self.draw()

    def draw(self):
        rows = self.x
        cols = self.y
        xmin = -(rows * self._size / 2)
        xmax = rows * self._size / 2
        ymin = -(cols * self._size / 2)
        ymax = cols * self._size / 2

        self.t.color('black', 'black')
    
        self.t.begin_fill()
        self.t.up()
        self.t.goto(xmin, ymin)
        self.t.down()
        self.t.setheading(90)
        for d in (self.y*self._size, self.x*self._size, self.y*self._size, self.x*self._size):
            self.t.forward(d)
            self.t.right(90)
        self.t.end_fill()
        self.t.up()
    
        self.t.color('red', 'black')
        self.t.goto(xmin, ymin)
        for col in range(cols+1):
            self.t.down()
            self.t.setx(xmax)
            self.t.up()
            self.t.setx(xmin)
            self.t.sety(self.t.ycor() + self._size)
            self.update()
    
        self.t.goto(xmin, ymin)
        for row in range(rows+1):
            self.t.down()
            self.t.sety(ymax)
            self.t.up()
            self.t.sety(ymin)
            self.t.setx(self.t.xcor() + self._size)
            self.update()

    def _to_cell(self, x, y):
        self.t.up()
        self.t.goto(x*self._size - (self.x*self._size/2), y*self._size - (self.y*self._size/2))

    def color_cell(self, x, y, line, fill):
        for num, limit in (x, self.x), (y, self.y):
            if num < 0 or num >= limit:
                raise ValueError("Cell coordinate {} out of range {}-{}".format(num, 0, limit-1))
        self._to_cell(x, y)
        self.t.color(line, fill)
        self._fill_square()
        self.update()

    def _fill_square(self):
        self.t.begin_fill()
        self.t.setheading(90)
        self.t.down()
        for i in range(4):
            self.t.forward(self._size)
            self.t.right(90)
        self.t.up()
        self.t.end_fill()

    def update(self):
        self.screen.update()
        time.sleep(self.delay)

if __name__ == '__main__':
    test()
