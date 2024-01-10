def turn_to_list_maze(maze_file_path: str):
    arr_maze = []
    with open(maze_file_path, 'r') as maze:
        for line in maze.readlines():
            line_list = list(line)
            line_list.remove("\n")
            arr_maze.append(line_list)
    return arr_maze


if __name__ == "__main__":
    pass
