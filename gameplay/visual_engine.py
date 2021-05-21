from sys import exit

import pygame
import numpy as np

from alpha_template.constants.constants import *

class coords:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class segment:
    def __init__(self, type_, rect, clicked, color):
        self.type_ = type_
        self.rect = rect
        self.clicked = clicked
        self.color = color



# TODO: Substitute your visual engine
class VisualEngine:
    def __init__(self):
        pygame.init()   # pylint: disable=no-member
        size = (rows * height + 5, cols * width + 5 + 30) # 5 epaisseur du trait  #30 zone de texte
        self.screen = pygame.display.set_mode(size)
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.font2 = pygame.font.Font('freesansbold.ttf', 20)

        self.grid = self.init_grid()
        # Check if useful
        a = segment('h', pygame.Rect((30, 30), (30, 30)), False, red)
        self.surf_grid = pygame.surfarray.make_surface(self.grid)
        self.surf_score = pygame.Surface([rows * height + 5, 30])
        self.surf_winner = pygame.Surface([rows * height + 5, cols * width + 5])

        self.horizontal_lines = pygame.Surface([rows * height + 5, cols * width + 5], pygame.SRCALPHA)
        self.vertical_lines = pygame.Surface([rows * height + 5, cols * width + 5], pygame.SRCALPHA)
        self.dots = pygame.Surface([rows * height + 5, cols * width + 5], pygame.SRCALPHA)

        self.h_segments = []
        self.v_segments = []

        for i in range(0, rows + 1):
            for j in range(0, cols + 1):
                pygame.draw.circle(self.dots, grey0, (i * height + 3, j * width + 3), 5)
                self.h_segments.append(segment('h', pygame.Rect((i * height, j * width), (width, 5)), False, grey3))
                self.v_segments.append(segment('v', pygame.Rect((i * height, j * width), (5, height)), False, grey3))
        self.surf_winner.fill(grey4)


    def init_grid(self):
        grid = np.full((rows * height, cols * width, 3), grey2)
        for i in range(0, rows):
            for j in range(0, cols):
                if i % 2 == 0:
                    if j % 2 == 0:
                        grid = self.fill_big(grid, i * width, j * height, grey1)
                else:
                    if j % 2 != 0:
                        grid = self.fill_big(grid, i * width, j * height, grey1)

        return grid

    def draw_board(self, board, ai_confidence: float = 0.5):
        for seg_data in self.v_segments:
            pygame.draw.rect(self.vertical_lines, seg_data.color, seg_data.rect)

        for seg_data in self.h_segments:
            pygame.draw.rect(self.horizontal_lines, seg_data.color, seg_data.rect)

        # winner
        surf_winner = pygame.Surface([rows * height + 5, cols * width + 5])
        surf_winner.fill(grey4)

        self.screen.blit(self.surf_grid, (0, 0))
        self.screen.blit(self.horizontal_lines, (0, 0))
        self.screen.blit(self.vertical_lines, (0, 0))
        self.screen.blit(self.dots, (0, 0))
        pygame.display.update()


    def draw_scores(self, score_p1, score_p2, turn, game_over=False):
        score1 = self.font.render(str(score_p1), True, blue)
        score2 = self.font.render(str(score_p2), True, green)

        self.screen.blit(self.surf_score, (0, cols * width + 5))
        # surf_score.blit(score, (3, 3))
        self.screen.blit(score1, (3, cols * width + 5 + 3))
        if score_p2 < 10:
            self.screen.blit(score2, (rows * height + 5 - 20, cols * width + 5 + 3))
        if score_p2 > 9:
            self.screen.blit(score2, (rows * height + 5 - 35, cols * width + 5 + 3))

        if game_over:
            if score_p1 == score_p2:
                winner_font = self.font2.render(f"Tie! ", True, (0, 0, 0))
            else:
                winner_font = self.font2.render(f"P{turn} Won", True, (0, 0, 0))

            self.screen.blit(self.surf_winner, (0, 0))
            self.screen.blit(winner_font, (cols * width / 2, rows * height / 2))  ###centrer
        pygame.display.update()


    @staticmethod
    def fill_big(grid, i, j, color):
        for k in range(0, width):
            for l in range(0, height):
                grid[i + k, j + l] = color
        return grid
