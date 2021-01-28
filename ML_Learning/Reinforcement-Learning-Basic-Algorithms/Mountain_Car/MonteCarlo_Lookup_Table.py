import numpy as np
import MountainCar_env

env = MountainCar_env.MountainCarEnv()
env._max_episode_steps = 1000

p_lvs = 5
v_lvs = 5
gamma = 0.999
Q = np.zeros((p_lvs, v_lvs, 3))
N = np.zeros((p_lvs, v_lvs, 3))

def mapping(observation):       # Transforming continous state into discrete state
    p, v = observation
    p_c = int((p+1.2)/(1.8/p_lvs))
    v_c = int((v+0.07)/(0.14/v_lvs))
    return [p_c, v_c]


for epi in range(5000):
    history = []
    observation = env.reset()
    state_tmp = mapping(observation)

    for t in range(env._max_episode_steps):
        if epi % 100 == 0: env.render()

        if np.random.rand() < 100/ (100 + epi):      # Exploration
            action = env.action_space.sample()
        else:
            action = np.argmax(Q[tuple(state_tmp)])     # Exploitation

        observation, _, done, _ = env.step(action)      # observation after taking the action

        reward = (1.0 + observation[0]) * (observation[0] > -0.2) + (10000 - 10 * t) * (observation[0] >= 0.5)      # new definition of reward

        state_tmp = mapping(observation)
        S_A_R = state_tmp + [action, reward]
        history.append(S_A_R)

        if done:
            if epi % 10 == 0: print("Episode {}: {} steps, {} return".format(epi + 1, t + 1, np.sum(
                np.array(history)[:, 3] * (gamma * np.ones(len(history))) ** np.arange(len(history)))))
            break

    rewards = np.array(history)[:, 3]
    t = 0
    T = len(history)
    for sar in history:
        sa = sar[:3]
        N[tuple(sa)] += 1
        G = np.sum(rewards[t:T] * (gamma * np.ones(T - t)) ** np.arange(T - t))

        # Q[tuple(sa)] += 1/N[tuple(sa)]*(G-Q[tuple(sa)])
        Q[tuple(sa)] += 0.001 * (G - Q[tuple(sa)])
        t += 1

env.close()





