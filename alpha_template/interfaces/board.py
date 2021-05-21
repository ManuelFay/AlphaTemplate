import numpy as np

# TODO: Change depending on your constants
from alpha_template.constants.constants import rows, cols


class Board:
    def __init__(self, board, turn):
        self.board = np.zeros((rows, cols)).astype(np.uint8) if board is None else board
        self.turn = turn
        self.count = 0
        self.score_p1 = 0
        self.score_p2 = 0

        self.last_move = None
        assert isinstance(self.board, np.ndarray)

    def update_turn(self):
        self.turn = 1 - self.turn

    # TODO: adapt to your game
    def play_action(self, row, col):
        """Update board after move"""
        self.board[row, col] = self.turn + 1

        # TODO: Here last move is the last action played - can be int, tuple
        self.last_move = (row, col)
        self.update_turn()

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
