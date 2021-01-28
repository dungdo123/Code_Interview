# Description: The objective is achieved after around 15 episodes

# Import the necessary libraries
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import sklearn.preprocessing
import MountainCar_env

# init mountain car environment
env = MountainCar_env.MountainCarEnv()

# init hyperparameters
num_episodes = 50
discount_factor = 1.0
alpha = 0.01
nA = env.action_space.n
nS = env.observation_space.shape[0]
print(nA)
print(nS)

# define parameters for linear approximation
w = np.zeros((nA, nS))

# init variables for plotting training process
plt_actions = np.zeros(nA)
episode_rewards = np.zeros(num_episodes)

# preparing for input state normalization
observation_examples = np.array([env.observation_space.sample() for x in range(10000)])
scaler = sklearn.preprocessing.StandardScaler()
scaler.fit(observation_examples)

# Normalize state function
def normalize_state(state):
    # transform data
    scaled = scaler.transform([state])
    return scaled

# Action-value function
def Q(state, action, W):
    value = state.dot(W[action])
    return value

# Epsilon greedy policy
def policy(state, weight, epsilon=0.1):
    A = np.ones(nA, dtype=float)*epsilon/nA
    best_action = np.argmax([Q(state, a, w) for a in range(nA)])
    A[best_action] += (1.0-epsilon)
    sample = np.random.choice(nA, p=A)
    return sample

# Main training loop
for epi in range(num_episodes):
    state = env.reset()
    state = normalize_state(state)
    t = 0

    while True:
        env.render()

        # Sample from our policy
        action = policy(state, w)
        t += 1

        # statistic for graphing
        plt_actions[action] += 1

        # Step environment and get next state and make it a feature
        next_state, reward, done, _ = env.step(action)
        next_state = normalize_state(next_state)

        # figure out what our policy tells us to do for the next state
        next_action = policy(next_state, w)

        # statistic for graphing
        episode_rewards[epi] += reward

        # figure out target and td error
        target = reward + discount_factor*Q(next_state, next_action, w)
        td_error = Q(state, action, w) - target

        # Find gradient with code to check it commented
        dw = (td_error).dot(state)

        # Update weight
        w[action] -= alpha*dw

        if done or t > 1000:
            print("Episode {}: {} steps, {} rewards".format(epi, t, episode_rewards[epi]))
            break

        # Update our state
        state = next_state

def plot_cost_to_go_mountain_car(num_tiles=20):
    x = np.linspace(env.observation_space.low[0], env.observation_space.high[0], num=num_tiles)
    y = np.linspace(env.observation_space.low[1], env.observation_space.high[1], num=num_tiles)
    X, Y = np.meshgrid(x, y)
    Z = np.apply_along_axis(lambda _: -np.max([Q(normalize_state(_), a, w) for a in range(nA)]), 2, np.dstack([X, Y]))

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=matplotlib.cm.coolwarm, vmin=-1.0, vmax=1.0)
    ax.set_xlabel('Position')
    ax.set_ylabel('Velocity')
    ax.set_zlabel('Value')
    ax.set_title("Mountain \"Cost To Go\" Function")
    fig.colorbar(surf)
    plt.show()

# Show bar graph of actions chosen
plt.bar(np.arange(nA),plt_actions)

plt.figure()
# Plot the reward over all episodes
plt.plot(np.arange(num_episodes),episode_rewards)
plt.show()
# plot our final Q function
plot_cost_to_go_mountain_car()

env.close()