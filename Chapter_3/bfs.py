from mazify import turn_to_list_maze
from collections import deque

maze = turn_to_list_maze("maze.txt")


class Node:
    def __init__(self, row, col, parent):
        self.row = row
        self.col = col
        self.parent = parent

    def get_parent(self):
        return self.parent


frontier = deque()


def at_boundaries(node):
    boundary_row = node.row < 0 or node.row > 20
    boundary_column = node.col < 0 or node.col > 20
    return boundary_row or boundary_column or (maze[node.row][node.col] == '*') or (maze[node.row][node.col] == '#')


def right(node):
    new_right_cord = node.col + 1
    new_right_node = Node(node.row, new_right_cord, node)
    if not at_boundaries(new_right_node):
        frontier.append(new_right_node)


def left(node):
    new_left_cord = node.col - 1
    new_left_node = Node(node.row, new_left_cord, node)
    if not at_boundaries(new_left_node):
        frontier.append(new_left_node)


def up(node):
    new_up_cord = node.row - 1
    new_up_node = Node(new_up_cord, node.col, node)
    if not at_boundaries(new_up_node):
        frontier.append(new_up_node)


def down(node):
    new_down_cord = node.row + 1
    new_down_node = Node(new_down_cord, node.col, node)
    if not at_boundaries(new_down_node):
        frontier.append(new_down_node)


def expand(node):
    right(node)
    left(node)
    up(node)
    down(node)
    maze[node.row][node.col] = "*"
    return frontier


def visited(node):
    maze[node.row][node.col] = "."


def is_goal(test_node, goal_node):
    return test_node.col == goal_node.col and test_node.row == goal_node.row


def bfs(initial_node, goal_node):
    node = initial_node
    if is_goal(node, goal_node):
        return initial_node
    frontier.append(node)
    while len(frontier) != 0:
        node = frontier.popleft()
        for child in expand(node):
            if is_goal(child, goal_node):
                return child


def make_path(initial_node, success):
    maze[success.row][success.col] = "%"

    while success != initial:
        maze[success.parent.row][success.parent.col] = "%"
        success = success.parent
    maze[initial_node.row][initial_node.col] = "%"


initial = Node(0, 0, None)
goal = Node(20, 19, None)
success_node = bfs(initial, goal)
make_path(initial, success_node)
print(maze)
