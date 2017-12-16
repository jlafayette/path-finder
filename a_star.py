from queue import PriorityQueue


def search(grid):
    print("starting {} search".format(__name__))
    # The set of nodes already evaluated
    # closedSet := {}  # block.visited

    # The set of currently discovered nodes that are not evaluated yet.
    # Initially, only the start node is known.
    # openSet := {start}
    start = grid.get_start_block()
    end = grid.get_end_block()
    open_queue = PriorityQueue()

    # For each node, which node it can most efficiently be reached from.
    # If a node can be reached from many nodes, cameFrom will eventually contain the
    # most efficient previous step.
    # cameFrom := an empty map    # add an attribute to block

    # For each node, the cost of getting from the start node to that node.
    # add attribute to block
    # gScore := map with default value of Infinity

    # The cost of going from start to start is zero.
    # gScore[start] := 0
    start.gscore = 0

    # For each node, the total cost of getting from the start node to the goal
    # by passing by that node. That value is partly known, partly heuristic.
    # fScore := map with default value of Infinity

    # For the first node, that value is completely heuristic.
    start.fscore = heuristic_cost_estimate(start, end)
    # fScore[start] := heuristic_cost_estimate(start, goal)
    open_queue.put(start)

    while not open_queue.empty():
        # current = the node in open_queue having the lowest fScore[] value
        current = open_queue.get()
        current.open = False
        redraw = [current]
        if grid.is_goal(current):
            yield redraw
            break
        current.visited = True
        for neighbor in grid.get_successors(current):
            if neighbor.visited:
                continue   # Ignore the neighbor which is already evaluated.
            tentative_gscore = current.gscore + dist_between(current, neighbor)
            if tentative_gscore >= neighbor.gscore:
                pass   # This is not a better path.
            else:
                neighbor.parent = current
                neighbor.gscore = tentative_gscore
                neighbor.fscore = neighbor.gscore + heuristic_cost_estimate(neighbor, end)
            if not neighbor.open:   # Discover a new node
                neighbor.open = True
                open_queue.put(neighbor)
                redraw.append(neighbor)
        yield redraw


def heuristic_cost_estimate(start, end):
    return abs(start.x - end.x) + abs(start.y - end.y)


def dist_between(current, neighbor):
    return 1
