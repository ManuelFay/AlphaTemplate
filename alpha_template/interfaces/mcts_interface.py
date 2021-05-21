import random
from alpha_template.engines.mcts import Node
from alpha_template.constants.constants import PLAYER_1, PLAYER_2

from alpha_template.interfaces.board import Board


class BoardTree(Board, Node):
    def __init__(self, board, turn):
        self.id_ = None
        super().__init__(board, turn)
        self.update_id()

    def create_child(self, row, col):
        child = BoardTree(self.board.copy(), turn=self.turn)
        child.play_action(row, col)
        child.update_id()
        return child

    def update_id(self):
        self.id_ = hash(self.board.tostring())

    def is_terminal(self):
        return self.winning_move(PLAYER_1) or self.winning_move(PLAYER_2) or len(self.get_valid_locations()) == 0

    def find_children(self):
        if self.is_terminal():  # If the game is finished then no moves can be made
            return set()
        # Otherwise, you can make a move in each of the empty spots
        childs = set()

        # TODO: Adapt to your game if needed
        for col, row in self.get_valid_locations():
            childs.add(self.create_child(row, col))

        return childs

    def find_random_child(self):
        if self.is_terminal():
            return None  # If the game is finished then no moves can be made

        # TODO: Adapt to your game if needed
        col, row = random.choice(self.get_valid_locations())
        return self.create_child(row, col)

    def reward(self):
        return 0.5 if len(self.get_valid_locations()) == 0 else 0

    def __hash__(self):
        return self.id_

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
