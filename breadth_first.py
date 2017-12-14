from queue import Queue


def search(grid):
    print("starting search")

    # a FIFO open_set
    open_queue = Queue()
    # open_set = set()

    # an empty set to maintain visited nodes
    # closed_set = set()
    # a dictionary to maintain meta information (used for path formation)
    # meta = dict()  # key -> (parent block, action to reach child)

    # initialize
    start = grid.get_start_block()
    print("start: {!r}".format(start))
    open_queue.put(start)

    while not open_queue.empty():
        parent_block = open_queue.get()
        parent_block.open = False
        redraw = [parent_block]
        if grid.is_goal(parent_block):
            yield redraw   # The last thing yielded
            break

        for child_block in grid.get_successors(parent_block):

            if child_block.visited:
                continue

            if not child_block.open:
                child_block.parent = parent_block
                child_block.open = True
                open_queue.put(child_block)
                redraw.append(child_block)
        parent_block.visited = True
        yield redraw   # Allows game to step through the solve


def construct_path(block):
    while True:
        block = block.parent
        if block is None:
            break
        else:
            yield block
