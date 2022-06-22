import pygame
import numpy as np
import gym
from gym_env.envs.AI import AIstep

size = 100
sw = size * 7
sh = size * 7
radius = int(size / 2 - 5)
x = 6
y = 7


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
        self.board = np.zeros((x,y), dtype=int)
        self.win = None
        # self.turn = 0
        self.action_space = gym.spaces.Discrete(7)
        # if self.win is None:
        #     pygame.init()
        #     pygame.display.init()
        #     self.win = pygame.display.set_mode((sw, sh))
        #     pygame.display.set_caption('Connect4')
        #     self.clock = pygame.time.Clock()
        # self.draw_board()


    def action(self, action, player):
        if player == 1:
            if self.board[5][action] == 0:
                row = self.get_next_open_row(action)
                self.board[row][action] = player
                # self.draw_board()
            else:
                return True
        elif player == 2:
            if self.board[5][action] == 0:
                row = self.get_next_open_row(action)
                self.board[row][action] = player
                # self.draw_board()
            else:
                self.action(self.action_space.sample(), player)

        
    def step(self, action):
        # reward = 0
        done = False
        result = 0
        incorrect = False
        for player in range(1,3):
            if player == 1:
                incorrect = self.action(action, player)
                if incorrect:
                    done = True
                    result = 4
                elif self.winning_move(player):
                    done = True
                    result = player
                    state = self.get_current_state()
                    return state, done, result
            elif player == 2:
                AIaction = AIstep(self.board)
                self.action(AIaction, player)


                # Random:

                # incorrect = self.action(self.action_space.sample(), player)
                
                # Player:

                # Played = False
                # while not Played:
                #     for event in pygame.event.get():
                #         if event.type == pygame.QUIT:
                #             run = False
                #             pygame.quit()
                #             quit()
                #         if event.type == pygame.MOUSEBUTTONDOWN:
                #             posx = event.pos[0]
                #             # Ask for Player 2 Input
                #             col = int(math.floor(posx / size))
                #             self.action(col, player)
                #             Played = True


                if self.winning_move(player):
                    done = True
                    result = player
                    state = self.get_current_state()
                    return state, done, result

        state = self.get_current_state()
        if 0 not in state:
            done = True
            result = 3
            return state, done, result

        return state, done, result

    def get_next_open_row(self, col):
        for r in range(6):
            if self.board[r][col] == 0:
                return r


    def winning_move(self, player):
        # Check horizontal locations for win
        for c in range(7 - 3):
            for r in range(6):
                if self.board[r][c] == player and self.board[r][c + 1] == player and self.board[r][c + 2] == player and self.board[r][c + 3] == player:
                    return True

        # Check vertical locations for win
        for c in range(7):
            for r in range(6 - 3):
                if self.board[r][c] == player and self.board[r + 1][c] == player and self.board[r + 2][c] == player and self.board[r + 3][c] == player:
                    return True

        # Check positively sloped diaganols
        for c in range(7 - 3):
            for r in range(6 - 3):
                if self.board[r][c] == player and self.board[r + 1][c + 1] == player and self.board[r + 2][c + 2] == player and self.board[r + 3][c + 3] == player:
                    return True

        # Check negatively sloped diaganols
        for c in range(7 - 3):
            for r in range(3, 6):
                if self.board[r][c] == player and self.board[r - 1][c + 1] == player and self.board[r - 2][c + 2] == player and self.board[r - 3][c + 3] == player:
                    return True

    def get_current_state(self):
        field = np.copy(self.board)
        return np.resize(field, (field.shape[0] * field.shape[1],))

    def reset(self):
        self.board = np.zeros((x, y), dtype=int)

    def render(self):
        if self.win is None:
            pygame.init()
            pygame.display.init()
            self.win = pygame.display.set_mode((sw, sh))
            pygame.display.set_caption('Connect4')
            self.clock = pygame.time.Clock()
            
        self.draw_board()

    def draw_board(self):
        for c in range(y):
            for r in range(x):
                pygame.draw.rect(self.win, BLUE, (c * size, r * size + size, size, size))
                pygame.draw.circle(self.win, BLACK, (
                    int(c * size + size / 2), int(r * size + size + size / 2)), radius)

        for c in range(y):
            for r in range(x):
                if self.board[r][c] == 1:
                    pygame.draw.circle(self.win, RED, (
                        int(c * size + size / 2), sh - int(r * size + size / 2)), radius)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(self.win, YELLOW, (
                        int(c * size + size / 2), sh - int(r * size + size / 2)), radius)
        pygame.display.update()
        self.clock.tick(60)

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
