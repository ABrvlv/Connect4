from gym.envs.registration import register

register(
    id='Connect4-v1',
    entry_point='gym_env.envs:Connect4Env',
    max_episode_steps=2000,
)