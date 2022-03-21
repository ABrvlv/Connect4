import torch
import random
import numpy as np
from game import Connect4
from collections import deque
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    
    def __init__(self):
        self.n_games = 0
        self.n_wins = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(7, 256, 7)
        self.trainer = QTrainer(self.model, lr = LR, gamma = self.gamma)

    def get_state(self, game):
        state = game.board
        return state

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0,0,0,0,0]
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0,7)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype = torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    agent = Agent()
    game = Connect4()
    while True:
        state_old = agent.get_state(game)
        
        final_move = agent.get_action(state_old)

        reward, done, winner = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            if winner == 1:
                agent.n_wins += 1
            agent.train_long_memory()

            agent.model.save()

            print('Game', agent.n_games, 'Record:', agent.n_wins)

            plot_scores.append(agent.n_wins)
            total_score += agent.n_wins
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()