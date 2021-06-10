# pylint: disable=no-member
import sys
import math
import random
import numpy as np

import pygame

from alpha_template.interfaces.board import Board
from alpha_template.constants.constants import *
from alpha_template.agents.base_agent import BaseAgent

from gameplay.visual_engine import VisualEngine


class Game:
    def __init__(self, agent0: BaseAgent = None, agent1: BaseAgent = None, enable_ui: bool = True):
        self.board = Board(board=None, turn=random.choice([0, 1]))
        self.game_over = False
        self.agent0 = agent0
        self.agent1 = agent1

        self.result = None
        self.visual_engine = None

        if enable_ui:
            self.visual_engine = VisualEngine()
            self.visual_engine.draw_board(self.board.board)
            self.visual_engine.draw_scores(self.board.score_p1, self.board.score_p2, self.board.turn)

    def make_move(self, x, y):
        if self.board.is_valid_location(x, y):
            self.board.play_action(x, y)
            if self.board.winning_move() or self.board.tie():  # Switch because replay upon win
                self.board.update_turn()
                if self.visual_engine:
                    self.visual_engine.draw_scores(self.board.score_p1, self.board.score_p2, self.board.turn, game_over=True)

                self.game_over = True
                self.result = 0.5 if self.board.tie() else self.board.turn

    def play(self):
        """ Game routine - call the visual engine, the UI, the AI and the board state."""

        while not self.game_over:

            if self.board.turn == PLAYER_1 and self.agent0 is not None:  # If it is the AI turn
                x, y = self.agent0.move(board=self.board.board, turn=self.board.turn, score_p1=self.board.score_p1, score_p2=self.board.score_p2)
                self.make_move(x, y)
                if self.visual_engine:
                    print(f"Agent 0 Confidence: {self.agent0.ai_confidence}")
                    self.visual_engine.draw_board(self.board.board, self.agent1.ai_confidence if self.agent1 else 0)
                    self.visual_engine.draw_scores(self.board.score_p1, self.board.score_p2, self.board.turn)
                # continue

            if self.board.turn == PLAYER_2 and self.agent1 is not None:  # If it is the AI turn
                x, y = self.agent1.move(board=self.board.board, turn=self.board.turn, score_p1=self.board.score_p1, score_p2=self.board.score_p2)
                self.make_move(x, y)
                if self.visual_engine:
                    print(f"Agent 1 Confidence: {self.agent1.ai_confidence}")
                    self.visual_engine.draw_board(self.board.board, self.agent1.ai_confidence if self.agent1 else 0)
                    self.visual_engine.draw_scores(self.board.score_p1, self.board.score_p2, self.board.turn)
                # continue

            if self.visual_engine:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        coord = self.visual_engine.detect_collision(event, self.board)
                        if coord:
                            self.make_move(*coord)
                        self.visual_engine.draw_board(self.board.board,
                                                      self.agent1.ai_confidence if self.agent1 else 0)

                self.visual_engine.draw_board(self.board.board, self.agent1.ai_confidence if self.agent1 else 0)
                self.visual_engine.draw_scores(self.board.score_p1, self.board.score_p2, self.board.turn)

        if self.visual_engine:
            self.visual_engine.draw_board(self.board.board, self.agent1.ai_confidence if self.agent1 else 0)
            self.visual_engine.draw_scores(self.board.score_p1, self.board.score_p2, self.board.turn, game_over=True)
            pygame.time.wait(3000)

        if self.agent0:
            self.agent0.kill_agent(result=self.result if self.result == 0.5 else int(self.result == 0))
        if self.agent1:
            self.agent1.kill_agent(result=self.result if self.result == 0.5 else int(self.result == 1))

        return self.result
