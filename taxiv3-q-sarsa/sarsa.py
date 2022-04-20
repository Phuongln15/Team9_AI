from q_learning import QLearning

class SARSA(QLearning):
    """
    Sarsa learning inheriting from Q learning
    """
    def _get_next_reward(self, state, action, reward, next_state):
        next_action = self.get_action(state)
        next_reward = (reward + self.gamma*self.Q_table[next_state, next_action])
        return next_reward
