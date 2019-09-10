import gym
import math

env = gym.make('MountainCar-v0')

INIT_STEPS = 4
SMALL_VELOCITY = 0.002

QUITE_RIGHT = 0.05 * 2
NEAR_FINISH = 0.05 * 14
NOT_FAST = 0.018

def choose_action(observation, count, prev_action):
    position, velocity = observation
    abs_pos = position + math.pi / 6;

    if count < INIT_STEPS:
        return prev_action

    action = 0 if abs(abs_pos) > 0 else 2
    if abs(velocity) < SMALL_VELOCITY and action != prev_action:
        return action

    if QUITE_RIGHT < abs_pos < NEAR_FINISH and velocity < NOT_FAST:
        return 0

    return 0 if velocity < 0 else 2


def play(env, render=False):
    observation = env.reset()
    result = 0
    
    action = 0 if (observation[0] + math.pi / 6) > 0 else 2
    for count in range(200):
        if render:
            env.render()
        action = choose_action(observation, count, action)
        observation, reward, done, info = env.step(action)
        result += reward
        if done:
            break
    return result
    

for i_epi in range(0):
    print(play(env, True))

magic = 100000
result = sum([play(env) for _ in range(magic)]) / magic
print(result)

env.close()
