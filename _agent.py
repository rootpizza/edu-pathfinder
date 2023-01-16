import random
from abc import abstractmethod, ABC

from _grid import Grid


class Agent(ABC):
    def __init__(self, grid):
        self.grid: Grid = grid
        self.row, self.column = self.grid.origin
        self.moves = []
        self.path = [self.position]

    @property
    def position(self):
        return self.row, self.column

    @property
    def nr_of_moves(self):
        return len(self.moves)

    def visited(self, row, column):
        return (row, column) in self.path

    def peek(self, direction: str):
        return self.grid.move(direction, self.row, self.column)

    def move(self, direction: str):
        if direction == 'up':
            return self.move_up()
        elif direction == 'down':
            return self.move_down()
        elif direction == 'left':
            return self.move_left()
        elif direction == 'right':
            return self.move_right()
        else:
            raise ValueError()

    def move_left(self):
        self.row, self.column = self.grid.move_left(self.row, self.column)
        self._update_logs_with_move('left')

    def move_right(self):
        self.row, self.column = self.grid.move_right(self.row, self.column)
        self._update_logs_with_move('right')

    def move_up(self):
        self.row, self.column = self.grid.move_up(self.row, self.column)
        self._update_logs_with_move('up')

    def move_down(self):
        self.row, self.column = self.grid.move_down(self.row, self.column)
        self._update_logs_with_move('down')

    def _update_logs_with_move(self, move):
        self.moves.append(move)
        self.path.append(self.position)

    def at_origin(self):
        return self.row, self.column == self.grid.origin

    def at_destination(self):
        return (self.row, self.column) == self.grid.destination

    def __repr__(self):
        grid_repr = self.grid.get_grid_for_repr()
        grid_repr[self.row, self.column] = grid_repr[self.row, self.column] + '_A'
        return repr(grid_repr)

    @abstractmethod
    def decide_move(self):
        pass


class RandomAgent(Agent):
    def decide_move(self):
        fate = random.random()
        if fate < .25:
            self.move_left()
        elif fate < .5:
            self.move_down()
        elif fate < .75:
            self.move_right()
        else:
            self.move_up()
            
class SmartAgent(Agent):
    def decide_move(self):
        pass
