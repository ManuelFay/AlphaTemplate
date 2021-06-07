# pylint: disable=not-callable, no-member, no-name-in-module

import torch

from alpha_template.interfaces.naive_nn import NaiveNet
from alpha_template.constants.constants import rows, cols


class NeuralInterface:
    def __init__(self, model_path=None):
        self.model = NaiveNet(num_rows=rows, num_cols=cols)
        if model_path:
            # print(f"Loading weights from {model_path}")
            self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

    def score(self, node):
        """Flip board so that agent is always with pieces #1
        Score is from the POV of the next to play"""
        board = node.board.copy()
        tmp_boards = torch.tensor(board)
        input_ = torch.zeros(3, *tmp_boards.shape, dtype=torch.float32)

        # TODO: Adapt to your game
        input_[0, tmp_boards == 2] = 1
        input_[1, tmp_boards == 3] = 1
        input_[2, tmp_boards == 4] = 1

        if node.turn == 1:
            input_ = input_[[0, 2, 1], :]

        col_evaluation, score_evaluation = self.model(input_.unsqueeze(0))
        score = score_evaluation.squeeze().item()
        policy = col_evaluation.squeeze().detach().cpu().numpy()
        return score, policy
