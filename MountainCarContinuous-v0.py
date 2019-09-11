import gym
import math

env = gym.make('MountainCarContinuous-v0')

SMALL_INIT_POS_RIGHT = 0.040
SMALL_INIT_POS_LEFT = -0.030

INIT_STEPS_COMMON = 19
INIT_STEPS_SMALL_POS = 38
INIT_SPEED = 0.6
COMMON_SPEED = 0.75

SMALL_VELOCITY = 0.001
QUITE_RIGHT = 0.05 * 5
NEAR_FINISH = 0.05 * 10
NOT_FAST = 0.020

REALLY_FAST_LEFT = -0.035
REALLY_FAST_RIGHT = 0.045


def choose_action(observation, count, prev_action, init_steps):
    position, velocity = observation
    abs_pos = position + math.pi / 6

    if count < init_steps:
        return prev_action

    # slow down before finish
    if abs_pos < 0 and abs(velocity) > 0.05:
        return 0
    if (abs_pos > 0.6 and velocity > 0.03) \
            or (abs_pos > 0.7 and velocity > 0.02) \
            or (abs_pos > 0.8 and velocity > 0.005):
        return 0

    action = -COMMON_SPEED if abs(abs_pos) > 0 else COMMON_SPEED
    if abs(velocity) < SMALL_VELOCITY:
        return action

    if QUITE_RIGHT < abs_pos < NEAR_FINISH and velocity < NOT_FAST:
        return -COMMON_SPEED

    if REALLY_FAST_RIGHT < velocity or velocity < REALLY_FAST_LEFT:
        return 0

    return -COMMON_SPEED if velocity < 0 else COMMON_SPEED


def init(observation):
    abs_pos = (observation[0] + math.pi / 6)
    if SMALL_INIT_POS_RIGHT < abs_pos or abs_pos < SMALL_INIT_POS_LEFT:
        action = -INIT_SPEED if abs_pos > 0 else INIT_SPEED
        init_steps = INIT_STEPS_COMMON
    else:
        action = INIT_SPEED
        init_steps = INIT_STEPS_SMALL_POS
    return action, init_steps


def play(env, render=False):
    result = 0
    observation = env.reset()

    action, init_steps = init(observation)
    for count in range(200):
        if render:
            env.render()
        action = choose_action(observation, count, action, init_steps)
        observation, reward, done, info = env.step([action])
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
