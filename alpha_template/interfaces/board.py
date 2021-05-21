import numpy as np
from scipy.signal import convolve2d

from alpha_template.constants.constants import rows, cols, PLAYER_2, PLAYER_1


class Board:
    def __init__(self, board, turn):
        self.board = self.init_array() if board is None else board
        self.turn = turn
        self.count = 0
        self.score_p1 = 0
        self.score_p2 = 0

        self.last_move = None
        assert isinstance(self.board, np.ndarray)

    @staticmethod
    def init_array():
        game_array = np.zeros((rows * 2 + 1, cols * 2 + 1))
        for i in range(0, rows * 2 + 1):
            for j in range(0, cols * 2 + 1):
                if i % 2 == 0 and  j % 2 == 0:
                        game_array[i, j] = -1

                elif i % 2 == 1 and  j % 2 == 1:
                        game_array[i, j] = 0
                else:
                    game_array[i, j] = 1
        return game_array

    def check_new_cells(self):
        kernel = np.array([[0, 1, 0],
                           [1, 0, 1],
                           [0, 1, 0]])

        output  = np.nonzero(convolve2d(self.board >= 2, kernel, mode="same") == 4)
        output = [(x,y) for x,y in zip(*output) if self.board[x, y] == 0]
        return output

    def update_turn(self):
        self.turn = 1 - self.turn

    # TODO: adapt to your game
    def play_action(self, row, col):
        """Update board after move"""

        # Can be removed for speed
        if self.board[row, col] != 1:
            return False, []

        self.board[row, col] = 2
        coords = self.check_new_cells()  # est ce qu un carre a ete forme

        for x, y in coords:
            self.board[x, y] = 3 if self.turn == PLAYER_1 else 4

        self.last_move = (row, col)
        self.update_turn()
        return coords


    # TODO: adapt to your game. Actions may be encoded with a (row, col) tuple instead of just col
    def is_valid_location(self, action) -> bool:
        """Check if the action is possible: (ie. No one played there before)
        Return boolean value"""
        row, col = action
        return self.board[row, col] == 0

    def __str__(self):
        return np.flip(self.board, 0).tostring()

    # TODO: adapt to your game
    def winning_move(self, piece):
        """Detect if game is won"""
        if "game is over":
            return True
        return False

    # TODO: Not all games can tie
    def tie(self):
        """Detect if the gampe is a tie
        Here it checks if board is full, different games may have different tie condictions"""
        return not (self.board == 0).any()

    # TODO: adapt to your game
    def get_valid_locations(self):
        """Return valid actions to play
        Actions can be encoded as ints, tuples, etc..."""
        valid_actions = [(5, 2), (3, 4)]    # example 1
        # valid_actions = np.where(self.board[-1, :] == 0)[0]   # example 2
        return valid_actions
