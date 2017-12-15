import pygame

import breadth_first
import color
from grid import Grid


SCREEN_SIZE = (800, 800)


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    done = False
    refresh = False
    step_mode = False
    # x = 30
    # y = 30
    grid = Grid(screen, 40, 40, 16, SCREEN_SIZE)

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
        screen.fill(color.BLACK)
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
