# pylint: disable=no-member
import sys
import math
import random

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

    # TODO: Adapt to your game
    def make_move(self, col):
        if self.board.is_valid_location(col):
            row = self.board.get_next_open_row(col)
            self.board.play_action(row, col)

            if self.board.winning_move((1-self.board.turn) + 1):
                self.board.update_turn()
                if self.visual_engine:
                    label = self.visual_engine.myfont.render(f"Player {self.board.turn} wins!!", 1,
                                                             YELLOW if self.board.turn else RED)
                    self.visual_engine.screen.blit(label, (40, 10))
                self.game_over = True
                self.result = self.board.turn

            elif self.board.tie():
                if self.visual_engine:
                    label = self.visual_engine.myfont.render("It's a tie!", 1, BLUE)
                    self.visual_engine.screen.blit(label, (40, 10))
                self.game_over = True
                self.result = 0.5

    def play(self):
        """ Game routine - call the visual engine, the UI, the AI and the board state."""

        while not self.game_over:

            if self.board.turn == 0 and self.agent0 is not None:  # If it is the AI turn
                col = self.agent0.move(board=self.board.board, turn=self.board.turn)
                self.make_move(col)
                if self.visual_engine:
                    print(f"Agent 0 Confidence: {self.agent0.ai_confidence}")
                    self.visual_engine.draw_board(self.board.board, self.agent1.ai_confidence if self.agent1 else 0)
                continue

            if self.board.turn == 1 and self.agent1 is not None:  # If it is the AI turn
                col = self.agent1.move(board=self.board.board, turn=self.board.turn)
                self.make_move(col)
                if self.visual_engine:
                    print(f"Agent 1 Confidence: {self.agent1.ai_confidence}")
                    self.visual_engine.draw_board(self.board.board, self.agent1.ai_confidence if self.agent1 else 0)
                continue

            # TODO: Adapt to your visual engine
            if self.visual_engine:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print('current player : ', self.board.turn)
                        print('count ', self.board.count)

                        for seg_data in self.visual_engine.h_segments + self.visual_engine.v_segments:
                            seg = seg_data.rect
                            if seg.collidepoint(event.pos):
                                if seg_data.clicked == True:
                                    print('deja cliuqe')
                                    break
                                else:
                                    seg_data.clicked = True
                                    if self.board.turn == PLAYER_1:
                                        seg_data.color = blue
                                    elif self.board.turn == PLAYER_2:
                                        seg_data.color = green

                                    success, coord, self.board.count = self.visual_engine.mouse_clic(seg_data, self.board.turn, self.board.count)
                                    if success:
                                        if self.board.turn == PLAYER_1:
                                            self.board.score_p1 += len(coord)
                                        elif self.board.turn == PLAYER_2:
                                            self.board.score_p2 += len(coord)

                                        for point in coord:
                                            print(point.x, point.y)
                                            self.visual_engine.grid = self.visual_engine.fill_big(self.visual_engine.grid, (point.x // 2) * width, (point.y // 2) * height,
                                                            blue2 if self.board.turn == PLAYER_1 else green2)

                                            self.visual_engine.surf_grid = pygame.surfarray.make_surface(self.visual_engine.grid)
                                        print("SCORE : BLUE = ", self.board.score_p1, ' PURPLE =', self.board.score_p2)

                                        if self.board.score_p1 + self.board.score_p2 == rows * cols:
                                            self.game_over = True
                                            break

                                    self.board.update_turn()


                    self.visual_engine.draw_board(self.board.board, self.agent1.ai_confidence if self.agent1 else 0)
                    self.visual_engine.draw_scores(self.board.score_p1, self.board.score_p2, self.board.turn)

        if self.visual_engine:
            self.visual_engine.draw_board(self.board.board, self.agent1.ai_confidence if self.agent1 else 0)
            self.visual_engine.draw_scores(self.board.score_p1, self.board.score_p2, self.board.turn)
            pygame.time.wait(3000)

        if self.agent0:
            self.agent0.kill_agent(result=self.result if self.result == 0.5 else int(self.result == 0))
        if self.agent1:
            self.agent1.kill_agent(result=self.result if self.result == 0.5 else int(self.result == 1))

        return self.result
