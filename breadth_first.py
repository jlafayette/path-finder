from queue import Queue


def search(grid):

    # a FIFO open_set
    open_queue = Queue()
    # node.open: Tracks membership in open queue.

    # node.visited: Maintain visited nodes.
    # node.parent: Maintain information used for path formation.

    start = grid.get_start_block()
    open_queue.put(start)

    while not open_queue.empty():
        current = open_queue.get()
        current.open = False
        redraw = [current]   # List of nodes to be redrawn at each step.
        if grid.is_goal(current):
            yield redraw   # The last thing yielded is the goal node.
            break

        for neighbor in grid.get_neighbors(current):

            if neighbor.visited:
                continue

            if not neighbor.open:
                neighbor.parent = current
                neighbor.open = True
                open_queue.put(neighbor)
                redraw.append(neighbor)
        current.visited = True
        yield redraw
