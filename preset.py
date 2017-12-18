class Standard(object):
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


class Large(Standard):
    speed_mult = 3
    x_num = 350
    y_num = 174
    block_size = 5
    buffer = 50
    allow_diagonals = True
    wall_percentage = 55