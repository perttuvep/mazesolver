from cell import Cell
from graphics import Window
from maze import Maze


def main():
    win = Window(1280, 720)

    maze = Maze(5, 5, 12, 3, 50, 50, win)
    maze.solve()
    win.wait_for_close()


main()
