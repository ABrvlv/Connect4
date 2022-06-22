from typing import Optional, Union

import numpy as np

import gym
from gym import logger, spaces
from gym.error import DependencyNotInstalled
from gym_env.envs.connect4 import Connect4


class Connect4Env(gym.Env[np.ndarray, Union[int, np.ndarray]]):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 50}

    def __init__(self):
        self.game = Connect4()
        self.state = None
        self.turn = 0
        
        low = np.zeros((6*7), dtype = int)
        high = np.full((6*7), 2, dtype=int)

        self.action_space = gym.spaces.Discrete(7)
        self.observation_space = gym.spaces.Box(low, high, dtype=int)

       
    def step(self, action):
        assert self.action_space.contains(action)
        assert self.state is not None, "Call reset before using step method."
        reward = 0

        self.state, done, result = self.game.step(action)
        self.turn += 1
        if done:
            if result == 1:
                reward = 22-self.turn
                self.turn = 0
                return np.array(self.state, dtype=int), reward, done, {}
            elif result == 2:
                reward = -22+self.turn
                self.turn = 0
                return np.array(self.state, dtype=int), reward, done, {}
            elif result == 3:
                reward = 0
                self.turn = 0
                return np.array(self.state, dtype=int), reward, done, {}
            elif result == 4:
                reward = -22
                self.turn = 0
                return np.array(self.state, dtype=int), reward, done, {}
        return np.array(self.state, dtype=int), reward, done, {}
       
    def reset(self, *, seed: Optional[int] = None, return_info: bool = False):
        super().reset(seed=seed)
        self.game.reset()
        state = np.array(self.game.get_current_state(), dtype=int)
        self.state = state

        if not return_info:
            return np.array(self.state, dtype=int)
        else:
            return np.array(self.state, dtype=int), {}

    def render(self, mode="human"):
        assert self.state is not None, "Call reset before using render method."
        self.game.render()


    def close(self):
        import pygame
        pygame.display.quit()
        pygame.quit()