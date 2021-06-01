import numpy as np
from scipy.signal import convolve2d

from alpha_template.constants.constants import rows, cols, PLAYER_2, PLAYER_1


class Board:
    def __init__(self, board, turn, score_p1=0, score_p2=0):
        self.board = self.init_array() if board is None else board
        self.turn = turn
        self.score_p1 = score_p1
        self.score_p2 = score_p2
        self.last_move = None
        self.kernel = np.array([[0, 1, 0],
                                [1, 0, 1],
                                [0, 1, 0]])
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
        output  = np.nonzero(convolve2d(self.board >= 2, self.kernel, mode="same") == 4)
        coords = [(x,y) for x,y in zip(*output) if self.board[x, y] == 0]

        for x, y in coords:
            self.board[x, y] = 3 if self.turn == PLAYER_1 else 4

        return coords

    def update_turn(self):
        self.turn = 1 - self.turn

    # TODO: adapt to your game
    def play_action(self, x, y):
        """Update board after move"""
        # Can be removed for speed
        if not self.is_valid_location(x, y):
            print(f"Unvalid line ({x, y})")
            return

        self.board[x, y] = 2
        coords = self.check_new_cells()  # est ce qu un carre a ete forme

        if self.turn == PLAYER_1:
            self.score_p1 += len(coords)
        else:
            self.score_p2 += len(coords)

        self.last_move = (x, y)

        if len(coords) == 0:
            self.update_turn()

    # TODO: adapt to your game. Actions may be encoded with a (x, y) tuple instead of just col
    def is_valid_location(self, x, y) -> bool:
        """Check if the action is possible: (ie. No one played there before)
        Return boolean value"""
        return self.board[x, y] == 1

    def __str__(self):
        return np.flip(self.board, 0).tostring()

    def winning_move(self):
        """Detect if game is won
        Here it means that the player that just played has won more than half of the squares"""
        return max(self.score_p2, self.score_p1) > rows*cols/2

    def tie(self):
        """Detect if the game is a tie
        Here it checks if board is full and score indeterminate, different games may have different tie condictions"""
        return (not (self.board == 0).any()) and (not self.winning_move())

    def get_valid_locations(self):
        """Return valid actions to play
        Actions can be encoded as ints, tuples, etc..."""
        valid_actions = list(zip(*np.nonzero(self.board == 1)))
        return valid_actions
