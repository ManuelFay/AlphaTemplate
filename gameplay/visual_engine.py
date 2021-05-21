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
        self.game_array = self.init_array()

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

    @staticmethod
    def init_array():
        game_array = np.zeros((rows * 2 + 1, cols * 2 + 1))
        for i in range(0, rows * 2 + 1):
            for j in range(0, cols * 2 + 1):
                if i % 2 == 0:
                    if j % 2 == 0:
                        game_array[i, j] = 1
                else:
                    if j % 2 != 0:
                        game_array[i, j] = 1
        return game_array

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


    def draw_scores(self, score_p1, score_p2, turn):
        score1 = self.font.render(str(score_p1), True, blue)
        score2 = self.font.render(str(score_p2), True, green)

        winner_font = self.font2.render(f"{turn} Won", True, (0, 0, 0))  ###
        self.screen.blit(self.surf_score, (0, cols * width + 5))
        # surf_score.blit(score, (3, 3))
        self.screen.blit(score1, (3, cols * width + 5 + 3))
        if score_p2 < 10:
            self.screen.blit(score2, (rows * height + 5 - 20, cols * width + 5 + 3))
        if score_p2 > 9:
            self.screen.blit(score2, (rows * height + 5 - 35, cols * width + 5 + 3))

        if score_p1 + score_p2 == rows * cols:
            self.screen.blit(self.surf_winner, (0, 0))
            self.screen.blit(winner_font, (cols * width / 2, rows * height / 2))  ###centrer
        pygame.display.update()


    @staticmethod
    def fill_big(grid, i, j, color):
        for k in range(0, width):
            for l in range(0, height):
                grid[i + k, j + l] = color
        return grid

    def mouse_clic(self, seg_data, CURRENT_PLAYER, count):
        segment = seg_data.rect
        x, y = segment.centerx, segment.centery
        x = int(x // (height / 2))
        y = int(y // (width / 2))
        print('coord segmnent =', x, y)  # retranscription de coord game array

        self.game_array[x, y] = 2

        succes, coords = self.check_cell(x, y, seg_data)  # est ce qu un carre a ete forme
        if succes:
            if CURRENT_PLAYER == PLAYER_1:
                for coord in coords:
                    self.game_array[coord.x, coord.y] = 3
            elif CURRENT_PLAYER == PLAYER_2:
                for coord in coords:
                    self.game_array[coord.x, coord.y] = 4
            return True, coords, count
        else:
            count += 1
            return False, coords, count

    def remplissage_ou_pas(self, x, y):
        if self.game_array[x - 1, y] == 2 and self.game_array[x, y - 1] == 2 and self.game_array[x + 1, y] == 2 and self.game_array[x, y + 1] == 2:
            return True
        return False

    def check_cell(self, x, y, seg_data):
        coords_cases_remplies = []
        succes = 0
        # on verifie seulement les cases adjacentes pour economiser du calcul
        constraint = 0
        yesboy = 0

        if x == 0 or x == rows * 2:
            constraint += 1
        if y == 0 or y == cols * 2:
            constraint += 1

        if seg_data.type_ == 'h':
            if (y + 1) <= cols * 2 and self.remplissage_ou_pas(x, y + 1):
                coords_cases_remplies.append(coords(x, y + 1))
                yesboy += 1

            if (y - 1) >= 0 and self.remplissage_ou_pas(x, y - 1):
                coords_cases_remplies.append(coords(x, y - 1))
                yesboy += 1

        elif seg_data.type_ == 'v':
            if (x + 1) <= rows * 2 and self.remplissage_ou_pas(x + 1, y):
                coords_cases_remplies.append(coords(x + 1, y))
                yesboy += 1

            if (x - 1) >= 0 and self.remplissage_ou_pas(x - 1, y):
                coords_cases_remplies.append(coords(x - 1, y))
                yesboy += 1

        if yesboy >= 1:
            succes = 1
        return succes, coords_cases_remplies


