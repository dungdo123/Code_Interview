import numpy as np
import MountainCar_env

env = MountainCar_env.MountainCarEnv()
env._max_episode_steps = 1000

P_MAX = 0.6
P_MIN = -1.2
V_MAX = -0.07
V_MIN = 0.07
gamma = 0.999
alpha = 0.0001

n = 7
w = np.random.randn(n)

def get_x(observation, action):       # design a feature vector
    p, v = observation
    x = np.zeros(n)
    x[0] = (p - (P_MAX + P_MIN)/2)/(P_MAX-P_MIN)
    x[1] = (v - (V_MAX + V_MIN)/2)/(V_MAX-V_MIN)
    x[2] = x[1]**2
    x[3] = x[1]*(action-1)
    x[4+action] = 1
    return x

def e_greedy(observation, w, epi):      # e-greedy algorithm
    if np.random.rand() < 200 / (200 + epi):  # Exploration
        action = env.action_space.sample()
    else:
        Q_a0 = np.sum(get_x(observation, 0) * w)        # approximated action value for the action 0
        Q_a1 = np.sum(get_x(observation, 1) * w)        # approximated action value for the action 1
        Q_a2 = np.sum(get_x(observation, 2) * w)        # approximated action value for the action 2
        action = np.argmax([Q_a0, Q_a1, Q_a2])          # Exploitation
    return action

for epi in range(5000):
    observation = env.reset()
    history = []

    for t in range(env._max_episode_steps):
        if epi % 100 == 0: env.render()

        action = e_greedy(observation, w, epi)
        observation_new, _, done, _ = env.step(action)      # observation after taking the action
        reward = (1.0 + observation_new[0]) * (observation_new[0] > -0.2) + (10000 - 10 * t) * (observation_new[0] >= 0.5)  # new definition of reward

        S_A_R = [observation, action, reward]
        history.append(S_A_R)

        observation = observation_new*1
        if done: break

    if epi % 10 == 0:
        print("Episode {}: {} steps, {} return".format(epi + 1, t + 1, np.sum(np.array(history)[:, 2] * (gamma * np.ones(len(history))) ** np.arange(len(history)))))

    rewards = np.array(history)[:, 2]
    t = 0
    T = len(history)
    for sar in history:
        x = get_x(sar[0], sar[1])
        G = np.sum(rewards[t:T] * (gamma * np.ones(T - t)) ** np.arange(T - t))
        w += alpha*(G - np.sum(x*w))*x          # incremental weight update
        t += 1

env.close()