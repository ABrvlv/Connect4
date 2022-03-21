import pygame
import numpy as np
import math
import torch

pygame.init()

size = 100
sw = size * 7
sh = size * 7
radius = int(size / 2 - 5)


# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 100, 100)
GREEN = (100, 240, 100)
BLUE = (100, 100, 255)
GRAY = (128, 128, 128)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (170, 170, 170)
LIGHT_BLUE = (0, 0, 255)
LIGHT_RED = (255, 0, 0)
LIGHT_GREEN = (0, 255, 0)

class Connect4:

    def __init__(self):
        self.win = pygame.display.set_mode((sw, sh))
        pygame.display.set_caption('Connect4')
        self.reset()
        self.draw_board(self.board)


    def draw_board(self, board):
        for c in range(7):
            for r in range(6):
                pygame.draw.rect(self.win, BLUE, (c * size, r * size + size, size, size))
                pygame.draw.circle(self.win, BLACK, (
                    int(c * size + size / 2), int(r * size + size + size / 2)), radius)

        for c in range(7):
            for r in range(6):
                if board[r][c] == 1:
                    pygame.draw.circle(self.win, RED, (
                        int(c * size + size / 2), sh - int(r * size + size / 2)), radius)
                elif board[r][c] == 2:
                    pygame.draw.circle(self.win, YELLOW, (
                        int(c * size + size / 2), sh - int(r * size + size / 2)), radius)
        pygame.display.update()


    def get_next_open_row(self, board, col):
        for r in range(6):
            if board[r][col] == 0:
                return r


    def winning_move(self, board, piece):
        # Check horizontal locations for win
        for c in range(7 - 3):
            for r in range(6):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(7):
            for r in range(6 - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(7 - 3):
            for r in range(6 - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(7 - 3):
            for r in range(3, 6):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                    return True


    def get_step(self, action):
        return action

    def play_step(self, action):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action) # update the head
        pygame.time.wait(200)
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self.winning_move(self.board, self.turn%2):
            game_over = True
            reward = 10
            winner = self.turn%2
            return reward, game_over, winner

        # 4. place new food or just move
        self.turn += 1
        
        self.draw_board()

        # 6. return game over and score
        winner = 0
        return reward, game_over, winner


    def _move(self, action):
        col = action.index(1)
        

        if self.board[5][col] == 0:
            row = self.get_next_open_row(self.board, col)
            self.board[row][col] = 2
        else:
            pass

    def reset(self):
        self.board = np.zeros((6, 7))
        self.turn = 0

# def game():
#     board = np.zeros((6, 7))
#     turn = 0

#     run = True
#     draw_board(board)
#     while run:

#         # CONTROLS
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#                 pygame.quit()
#                 quit()
#             if event.type == pygame.MOUSEMOTION:
#                 pygame.draw.rect(win, BLACK, (0, 0, sw, size))
#                 posx = event.pos[0]
#                 col = int(math.floor(posx / size))
#                 if turn == 0:
#                     pygame.draw.circle(win, RED, (int(col * size + size * 0.5), int(size / 2)), radius)
#                 else:
#                     pygame.draw.circle(win, YELLOW, (int(col * size + size * 0.5), int(size / 2)), radius)
#             pygame.display.update()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 pygame.draw.rect(win, BLACK, (0, 0, sw, size))

#                 # Ask for Player 1 Input
#                 if turn == 0:
#                     col = int(math.floor(posx / size))

#                     if board[5][col] == 0:
#                         row = get_next_open_row(board, col)
#                         board[row][col] = 1
#                         if winning_move(board, 1):
#                             label = myfont.render("Player 1 wins", 1, RED)
#                             win.blit(label, (10, 10))

#                             reward += 10

#                             run = False
#                     else:
#                         turn += 1

#                 # # Ask for Player 2 Input
#                 else:
#                     posx = event.pos[0]
#                     col = action()

#                     if board[5][col] == 0:
#                         row = get_next_open_row(board, col)
#                         board[row][col] = 2
#                         if winning_move(board, 2):
#                             label = myfont.render("Player 2 wins", 1, RED)
#                             win.blit(label, (10, 10))
#                             run = False
#                     else:
#                         turn += 1

#                 print(np.flip(board, 0))
#                 draw_board(board)

#                 turn += 1
#                 turn = turn % 2
#             if not run:
#                 pygame.time.wait(3000)
