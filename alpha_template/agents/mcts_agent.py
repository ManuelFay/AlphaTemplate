# pylint: disable=too-many-instance-attributes

import os
import time
from typing import Optional
from tqdm import tqdm

import numpy as np
from alpha_template.agents.base_agent import BaseAgent
from alpha_template.engines.mcts import MCTS
from alpha_template.interfaces.mcts_interface import BoardTree


class MCTSAgent(BaseAgent):
    def __init__(self,
                 simulation_time: float = 3.,
                 training_path: Optional[str] = None,
                 show_pbar: bool = False):
        """is_training: weakens the agent to get more diverse training samples"""
        super().__init__()
        self.simulation_time = simulation_time
        self.tree = MCTS()
        self.training_path = training_path
        self.is_training = training_path is not None
        self.show_pbar = show_pbar and (not self.is_training)

        if self.is_training:
            self.boards = []
            self.policies = []

    def save_state(self, board):
        policy = self.tree.get_policy(board)
        board_ = board.board.copy()

        # Flip board so that agent always has pieces #1
        # TODO: Potentially adapt to your game
        if board.turn == 1:
            board_[board.board == 1] = 2
            board_[board.board == 2] = 1

        self.policies.append(policy)
        self.boards.append(board_)

    def estimate_confidence(self, board):
        """Confidence estimation assuming optimal adversary"""
        optimal_board = self.tree.choose(board)
        return self.tree.score(optimal_board)

    def move(self, board, turn):
        board = BoardTree(board, turn=turn)

        timeout_start = time.time()
        if self.show_pbar:
            pbar = tqdm()
        while time.time() < timeout_start + self.simulation_time:
            self.tree.do_rollout(board)
            if self.show_pbar:
                pbar.update()
        self.tree.unexplored_backlog = []

        if self.is_training:
            self.save_state(board)

        # TODO: Potentially adapt to your game and your board state representation
        # If less than 10 moves have been played and it's in training mode, play non optimal moves
        if (board.board != 0).sum() < 10 and self.is_training:
            optimal_board = self.tree.choose_stochastic(board, temperature=0.5)
        else:
            optimal_board = self.tree.choose(board)

        self.ai_confidence = self.estimate_confidence(board)

        # TODO: Last move is the last action played (can be int, tuple, etc)
        return optimal_board.last_move

    def kill_agent(self, result: float):
        """Store learning samples"""
        if self.is_training:
            training_samples = np.array([self.boards, self.policies, [result]*len(self.boards)], dtype=object)

            if os.path.isfile(self.training_path):
                train_ = np.load(self.training_path, allow_pickle=True)
                train_ = np.hstack((train_, training_samples))
            else:
                train_ = training_samples

            np.save(self.training_path, train_)
