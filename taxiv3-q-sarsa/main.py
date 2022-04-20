import os
import time
import gym
import sys
import math
import numpy as np
from matplotlib import pyplot as plt
from collections import deque
from q_learning import QLearning
from sarsa import SARSA

def create_agent(algo):
    if algo.upper() == "Q":
        return QLearning
    elif algo.upper() == "SARSA":
        return SARSA
    else:
        raise NameError("Please type either Q or Sarsa!")

def train_agent(env, agent, episodes=2000):
    """ Train agent.
    Params
    ======
    - env: instance of OpenAI Gym's Taxi-v3
    - agent: instance of class Agent
    - episodes: count of episodes to train agent
    Returns
    =======
    - avg_rewards: average rewards deque
    - best_avg_reward: largest value in the avg_rewards
    """
    # hyper-parameters
    Tmax = 100
    #episodes = 2000

    # measure performance
    average_rewards = deque(maxlen=episodes)
    # initialize best average reward
    best_avg_reward = -math.inf
    # initialize monitor for most recent rewards
    samp_rewards = deque(maxlen=Tmax)
    # for each episode
    for ep in range(1, episodes + 1):
        # begin episode
        state = env.reset()
        # initialize the sampled reward
        s = 0
        run = True
        while run:
            # select action
            action = agent.get_action(state)
            # perform selected action
            next_state, reward, done, info = env.step(action)
            # agent performs internal updates based on experience
            agent.step(state, action, reward, next_state, done)
            # update the sampled reward
            s += reward
            # update the state (s <- s') to next step
            state = next_state
            if done:
                # save final sampled reward
                samp_rewards.append(s)
                run = False
        if ep >= 100:
            # get average reward from last few episodes
            avg_r = np.mean(samp_rewards)
            # append to deque
            average_rewards.append(avg_r)
            # update best average reward
            if avg_r > best_avg_reward:
                best_avg_reward = avg_r
        # print progress

        if ep % 200 == 0 and ep > 0:
            print(f"\nEpisode {ep}/{episodes} || Best average reward {best_avg_reward}", end="")
            sys.stdout.flush()
            if ep == episodes:
                print('\n')
    return average_rewards, best_avg_reward

def plot_performance(env, algorithm, episodes):
    """
    Compare between Q and SARSA
    """
    plt.figure()
    plt.xlabel('Iterations')
    plt.ylabel(f'Average reward')
    print('Now executing: ' , algorithm)
    chosen_agent = create_agent(algorithm)
    agent = chosen_agent(env.observation_space.n, env.action_space.n)
    avg_rewards, best_avg_reward = train_agent(env, agent, episodes)
    plt.plot(avg_rewards)

    plt.legend(labels=algorithm, loc="lower right")
    plt.show()

def interact(env, agent):
    """
    Method to have the agent interact with environment
    Parameters
    ----------
    env - Taxi V3 environment
    agent - agent
    """
    while True:
        os.system("clear")
        state = env.reset()
        done = False
        while not done:
            action = agent.get_action(state)
            state, reward, done, info = env.step(action)
            # Put each rendered frame into dict for animation
            grid = env.render(mode='ansi')
            print(grid, end="")
            # sys.stdout.flush()
            time.sleep(1)
            os.system("clear")
        if input("Start a new episode (y/n): ").lower() == 'n':
            break


if __name__ == "__main__":
    env = gym.make('Taxi-v3')

    # train agents separately

    # if getting TERM variable not set, Edit configuration -> Environment Parameters: XTERM= xterm-color

    # -- run Q Learning agent --

    q_agent = create_agent("Q")
    q_agent = q_agent(env.observation_space.n, env.action_space.n)
    # trains agent
    q_avg_rewards, q_best_avg_reward = train_agent(env, q_agent, episodes=2000)
    # after training agent
    interact(env, q_agent)

    # -- run Sarsa agent --

    sarsa_agent = create_agent("SARSA")
    s_agent = sarsa_agent(env.observation_space.n, env.action_space.n)
    s_avg_rewards, s_best_avg_reward = train_agent(env, s_agent)
    interact(env, s_agent)


    # to visualize results

    # plot_performance(env, "Q", episodes=2000)
    # plot_performance(env, "Sarsa", episodes=2000)