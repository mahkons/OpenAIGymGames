import gym
import math

env = gym.make('MountainCar-v0')

SMALL_INIT_POS_RIGHT = 0.040
SMALL_INIT_POS_LEFT = -0.030

INIT_STEPS_COMMON = 4
INIT_STEPS_SMALL_POS = 13

SMALL_VELOCITY = 0.002
QUITE_RIGHT = 0.05 * 2
NEAR_FINISH = 0.05 * 14
NOT_FAST = 0.018


def choose_action(observation, count, prev_action, init_steps):
    position, velocity = observation
    abs_pos = position + math.pi / 6

    if count < init_steps:
        return prev_action

    action = 0 if abs(abs_pos) > 0 else 2
    if abs(velocity) < SMALL_VELOCITY and action != prev_action:
        return action

    if QUITE_RIGHT < abs_pos < NEAR_FINISH and velocity < NOT_FAST:
        return 0

    return 0 if velocity < 0 else 2


def init(observation):
    abs_pos = (observation[0] + math.pi / 6)
    if SMALL_INIT_POS_RIGHT < abs_pos or abs_pos < SMALL_INIT_POS_LEFT:
        action = 0 if abs_pos > 0 else 2
        init_steps = INIT_STEPS_COMMON
    else:
        action = 2
        init_steps = INIT_STEPS_SMALL_POS
    return (action, init_steps)


def play(env, render=False):
    observation = env.reset()
    result = 0
    action, init_steps = init(observation)
    for count in range(200):
        if render:
            env.render()
        action = choose_action(observation, count, action, init_steps)
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
