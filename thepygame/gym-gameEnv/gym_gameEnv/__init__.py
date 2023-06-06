from gym.envs.registration import register

register(
    id='gameEnv-v0',
    entry_point='gym_gameEnv.envs:GameEnv',
)
register(
    id='foo-extrahard-v0',
    entry_point='gym_gameEnv.envs:FooExtraHardEnv',
)