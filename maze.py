from graphics import Window
from cell import Cell
from time import sleep
import random


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed is not None:
            self.seed = random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = [
            [Cell(self.win) for y in range(self.num_rows)] for x in range(self.num_cols)
        ]

        for y in range(self.num_rows):
            for x in range(self.num_cols):
                self._draw_cell(x, y)

    def _draw_cell(self, col, row):
        if self.win is None:
            return
        x1 = self.x1 + col * self.cell_size_x
        y1 = self.y1 + row * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self._cells[col][row].draw(x1, y1, x2, y2)
        self._animate()

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        print(self._cells[0][0])
        self._draw_cell(0, 0)
        self._cells[-1][-1].has_bottom_wall = False
        print(self._cells[-1][-1])
        cells = self._cells
        print(len(cells), len(cells[1]))
        self._draw_cell(len(cells) - 1, len(cells[0]) - 1)

    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        sleep(0.01)

    def _break_walls_r(self, col, row):
        current = self._cells[col][row]
        current.visited = True
        cells = self._cells
        while True:
            left = 0
            right = 0
            up = 0
            down = 0
            possible = []
            if col > 0 and not cells[col - 1][row].visited:
                left = (col - 1, row)
                possible.append(left)

            if col < self.num_cols - 1 and not cells[col + 1][row].visited:
                right = (col + 1, row)
                possible.append(right)

            if row > 0 and not cells[col][row - 1].visited:
                up = (col, row - 1)
                possible.append(up)

            if row < self.num_rows - 1 and not cells[col][row + 1].visited:
                down = (col, row + 1)
                possible.append(down)

            if not possible:
                self._draw_cell(col, row)
                return

            next = possible[random.randrange(0, len(possible))]
            nextcell = self._cells[next[0]][next[1]]
            if next == left:
                current.has_left_wall = False
                nextcell.has_right_wall = False
            if next == right:
                current.has_right_wall = False
                nextcell.has_left_wall = False
            if next == up:
                current.has_top_wall = False
                nextcell.has_bottom_wall = False
            if next == down:
                current.has_bottom_wall = False
                nextcell.has_top_wall = False

            self._break_walls_r(next[0], next[1])

    def _reset_cells_visited(self):
        for y in range(self.num_rows):
            for x in range(self.num_cols):
                self._cells[x][y].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, col, row):
        self._animate()
        current = self._cells[col][row]
        current.visited = True

        if current == self._cells[-1][-1]:
            return True
        cells = self._cells
        left = 0
        right = 0
        up = 0
        down = 0
        possible = []
        if col > 0 and not cells[col - 1][row].visited and not current.has_left_wall:
            left = (col - 1, row)
            possible.append(left)

        if (
            col < self.num_cols - 1
            and not cells[col + 1][row].visited
            and not current.has_right_wall
        ):
            right = (col + 1, row)
            possible.append(right)

        if row > 0 and not cells[col][row - 1].visited and not current.has_top_wall:
            up = (col, row - 1)
            possible.append(up)

        if (
            row < self.num_rows - 1
            and not cells[col][row + 1].visited
            and not current.has_bottom_wall
        ):
            down = (col, row + 1)
            possible.append(down)

        if not possible:
            return False

        for dir in possible:
            to_cell = self._cells[dir[0]][dir[1]]
            current.draw_move(to_cell)
            if self._solve_r(dir[0], dir[1]):
                return True
            else:
                current.draw_move(to_cell, undo=True)
        return False
