from queue import Queue


import game


def breadth_first_search(grid: game.Grid):
    # a FIFO open_set
    open_queue = Queue()
    open_set = set()
    # an empty set to maintain visited nodes
    closed_set = set()
    # a dictionary to maintain meta information (used for path formation)
    meta = dict()  # key -> (parent block, action to reach child)

    # initialize
    start = grid.get_start_block()
    meta[str(start)] = None
    open_queue.put(start)
    open_set.add(start)

    while not open_queue.empty():

        # print("start")

        parent_block = open_queue.get()
        # print("parent block: [{}][{}]".format(parent_block.x, parent_block.y))
        # print("type: {0.type_}".format(parent_block))

        open_set.remove(parent_block)

        if grid.is_goal(parent_block):
            return construct_path(parent_block, meta)

        for child_block in grid.get_successors(parent_block):

            if child_block in closed_set:
                continue

            if child_block not in open_set:
                # print("meta keys: {}".format(meta.keys()))
                # print("adding key: {!s}".format(child_block))
                meta[str(child_block)] = parent_block
                open_queue.put(child_block)
                open_set.add(child_block)

        closed_set.add(parent_block)


def construct_path(block, meta):
    # print("start of construct_path")
    # print("block: {!r}".format(block))
    # print("meta: {!r}".format(meta))
    #
    # for k in sorted(list(meta.keys())):
    #     print("{!s} --> {!s}".format(k, meta[k]))

    block_list = list()
    while True:
        try:
            block = meta[str(block)]
            # print(repr(block))
            block_list.append(block)
        except KeyError as exc:
            # print("AttributeError: {}".format(exc))
            break
    # print("end of construct_path")
    return reversed(block_list)
