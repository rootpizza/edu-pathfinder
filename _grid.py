import random

import numpy as np



class GridFullException(Exception):
    pass


class Grid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self._obstacles_grid = np.zeros(shape=(self.rows, self.columns))
        self.origin = self._get_random_cell()
        self.destination = self.origin
        while self.destination == self.origin:
            self.destination = self._get_random_cell()

    @property
    def full(self):
        return self._obstacles_grid.sum() + 2 == self.rows * self.columns

    @property
    def obstacles(self):
        return list(zip(self._obstacles_grid.nonzero()[0], self._obstacles_grid.nonzero()[1]))

    def move(self, direction: str, row, column):
        if direction == 'up':
            return self.move_up(row, column)
        elif direction == 'down':
            return self.move_down(row, column)
        elif direction == 'left':
            return self.move_left(row, column)
        elif direction == 'right':
            return self.move_right(row, column)
        else:
            raise ValueError()

    def move_left(self, row, column):
        if column == 0 or self._obstacle_at_cell(row, column - 1):
            return row, column
        else:
            return row, column - 1

    def move_right(self, row, column):
        if column == self.columns - 1 or self._obstacle_at_cell(row, column + 1):
            return row, column
        else:
            return row, column + 1

    def move_up(self, row, column):
        if row == 0 or self._obstacle_at_cell(row - 1, column):
            return row, column
        else:
            return row - 1, column

    def move_down(self, row, column):
        if row == self.rows - 1 or self._obstacle_at_cell(row + 1, column):
            return row, column
        else:
            return row + 1, column

    def add_random_obstacle(self):
        if self.full:
            raise GridFullException()
        row, column = self._get_random_free_cell()
        self._add_obstacle_at_cell(row, column)

    def add_random_obstacles(self, nr_obstacles):
        for x in range(nr_obstacles):
            self.add_random_obstacle()

    def _get_random_free_cell(self):
        if self.full:
            raise GridFullException()
        row, column = self._get_random_cell()
        while self._occupied(row, column):
            row, column = self._get_random_cell()
        return row, column

    def _occupied(self, row, column):
        return \
            self.origin == (row, column) or \
            self.destination == (row, column) or \
            self._obstacle_at_cell(row, column)

    def _obstacle_at_cell(self, row, column):
        return self._obstacles_grid[row][column] == 1

    def _add_obstacle_at_cell(self, row, column):
        self._obstacles_grid[row][column] = 1

    def _remove_obstacle_at_cell(self, row, column):
        self._obstacles_grid[row][column] = 0

    def _get_random_cell(self):
        return random.randint(0, self.rows - 1), random.randint(0, self.columns - 1)

    def get_grid_for_repr(self):
        obs_list = self._obstacles_grid.tolist()
        obs_list[self.origin[0]][self.origin[1]] = 'ORIG'
        obs_list[self.destination[0]][self.destination[1]] = 'DEST'
        return np.array(obs_list)

    def __repr__(self):
        return repr(self.get_grid_for_repr())
