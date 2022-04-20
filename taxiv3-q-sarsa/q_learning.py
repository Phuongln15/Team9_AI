import numpy as np

class QLearning:
    """
    Q Learning RL method
    """
    def __init__(self, states_c, actions_c, epsilon = 1.0, min_epsilon = 0.005, alpha = 0.2, gamma = 0.99):
        self.min_epsilon = min_epsilon
        self.epsilon = epsilon # exploration vs exploitation
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount factor
        self.states_c = states_c
        self.actions_c = actions_c
        self.Q_table = np.zeros((self.states_c, self.actions_c))
        self.episode = 0

    def epsilon_greedy(self, state):
        """
        Returns the policy of the agent in current state using epsilon-greedy algorithm
        Parameters
        ----------
        state - current state of agent
        Returns
        -------
        pi policy
        """
        # pi as policy with random equal probabilities
        pi = np.full((self.actions_c), 1.0 * self.epsilon/ (self.actions_c))
        # get best action of state
        best_action = np.argmax(self.Q_table[state, :])
        # update the value the best action
        pi[best_action] += 1.0 - self.epsilon
        return pi

    def get_action(self, state):
        '''
        Returns an action using epsilon-greedy policy
        Parameters
        ----------
        state: current state of agent

        Returns
        -------
        best action using epsilon greedy
        '''
        policy = self.epsilon_greedy(state)
        action = np.random.choice(np.arange(self.actions_c), p=policy)
        return action
    

    def get_next_reward(self, reward, next_state):
        next_reward = reward + self.gamma * np.max(self.Q_table[next_state, :])
        return next_reward


    def step(self, state, action, reward, next_state, done):
        """
        Updates agent's knowledge after step
        Parameters
        ----------
        state - previous state of agent
        action - previous action of environment
        reward - last reward received
        next_state - current state of environment
        done - boolean, true if episode is complete and false if not
        -------

        """
        # update state-action function
        next_reward = self.get_next_reward(reward, next_state)
        q_value = ((1 - self.alpha) * self.Q_table[state, action]) + (self.alpha * next_reward)
        self.Q_table[state, action] = q_value
        if done:
            # decrease epsilon value to encourage exploration and maximize reward sum
            self.episode += 1
            self.epsilon = max(1./self.episode, self.min_epsilon) # min epsilon 0.005