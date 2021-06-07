import random
from alpha_template.engines.mcts import Node

from alpha_template.interfaces.board import Board


class BoardTree(Board, Node):
    def __init__(self, board, turn, **args):
        self.id_ = None
        super().__init__(board, turn, **args)
        self.update_id()

    def create_child(self, x, y):
        child = BoardTree(self.board.copy(), turn=self.turn, score_p1=self.score_p1, score_p2=self.score_p2)
        child.play_action(x, y)
        child.update_id()
        return child

    def update_id(self):
        self.id_ = hash(self.board.tostring())

    def is_terminal(self):
        return self.winning_move() or self.tie()

    def find_children(self):
        if self.is_terminal():  # If the game is finished then no moves can be made
            return set()
        # Otherwise, you can make a move in each of the empty spots
        childs = set()

        # TODO: Adapt to your game if needed
        for x, y in self.get_valid_locations():
            childs.add(self.create_child(x, y))

        return childs

    def find_random_child(self):
        if self.is_terminal():
            return None  # If the game is finished then no moves can be made

        # TODO: Adapt to your game if needed
        x, y = random.choice(self.get_valid_locations())
        return self.create_child(x, y)

    def reward(self):
        return 0.5 if self.tie() else 1


    def __hash__(self):
        return self.id_

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
