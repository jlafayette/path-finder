import math
from queue import PriorityQueue


def search(grid):
    print("starting {} search".format(__name__))
    # node.visited: The set of nodes already evaluated.

    # The set of currently discovered nodes that are not evaluated yet.
    # Initially, only the start node is known.
    start = grid.get_start_block()
    end = grid.get_end_block()
    open_queue = PriorityQueue()

    # node.parent: For each node, which node it can most efficiently be reached from.
    # If a node can be reached from many nodes, parent will eventually contain the
    # most efficient previous step.

    # node.gscore: For each node, the cost of getting from the start node to that node. It gets a
    # a default value of Infinity

    # The cost of going from start to start is zero.
    start.gscore = 0

    # node.fscore: For each node, the total cost of getting from the
    # start node to the goal by passing by that node. That value is
    # partly known, partly heuristic. It gets a default value of
    # Infinity.

    # For the first node, that value is completely heuristic.
    start.fscore = heuristic_cost_estimate(start, end)
    open_queue.put(start)

    while not open_queue.empty():
        current = open_queue.get()   # Node in open_queue having the lowest fScore value
        current.open = False
        redraw = [current]   # List of nodes to be redrawn at each step.
        if grid.is_goal(current):
            yield redraw
            break
        current.visited = True
        for neighbor in grid.get_neighbors(current):
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
    return math.sqrt((neighbor.x - current.x)**2 + (neighbor.y - current.y)**2)
