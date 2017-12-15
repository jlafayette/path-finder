BLUE = (0, 128, 255)
ORANGE = (255, 100, 0)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)


def tint(color, amount=50):
    result = [min(component + amount, 255) for component in color]
    return tuple(result)


def shade(color, amount=50):
    result = [max(component - amount, 0) for component in color]
    return tuple(result)


BLUE_TINT = tint(BLUE)
BLUE_SHADE = shade(BLUE)
YELLOW_SHADE = shade(YELLOW)
RED_SHADE = shade(RED)
GREEN_SHADE = shade(GREEN)
GREY_SHADE = shade(GREY)