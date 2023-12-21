import numpy as np

############################### 환경 : 에이전트의 액션을 받아 상태변이를 일으키고, 보상을 줌
class Environment:
    def __init__(self, random_speed):
        self.random_speed = random_speed

    def step(self, action):
        pass
        # 액션과 보상을 작성
        # return (new state), reward, done

    # 필요한 액션에 대한 함수 작성



############################### 에이전트 : 정책을 따라 움직임
class QLearningAgent:
    def __init__(self, num_actions, learning_rate, discount_factor, exploration_prob):
        self.num_actions      = num_actions
        self.learning_rate    = learning_rate
        self.discount_factor  = discount_factor
        self.exploration_prob = exploration_prob
        self.q_table          = np.zeros((num_actions, num_actions))

    def select_action(self, state):
        if np.random.uniform(0, 1) < self.exploration_prob:
            return np.random.randint(self.num_actions)
        else:
            return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state):
        predict                      = self.q_table[state, action]
        target                       = reward + self.discount_factor * np.max(self.q_table[next_state])
        self.q_table[state, action] += self.learning_rate * (target - predict)

# Define hyperparameters
num_actions      = 11  # Number of discrete actions for c (e.g., from 0 to 1 with step size 0.1)
learning_rate    = 0.1
discount_factor  = 0.9
exploration_prob = 0.1
num_episodes     = 1000

# Initialize environment and agent
env   = Environment(random_speed=True)
agent = QLearningAgent(num_actions, learning_rate, discount_factor, exploration_prob)

# Training loop
for episode in range(num_episodes):
    state        = 0  # Define state based on environment and agent representation
    total_reward = 0

    while not done:
        action = agent.choose_action(state)
        next_state, reward, done = env.step(action)
        agent.update_q_table(state, action, reward, next_state)
        state = next_state
        total_reward += reward

    print(f"Episode {episode}, Total Reward: {total_reward}")

# After training, retrieve the optimal action (c) and predicted fov region
optimal_action       = np.argmax(agent.q_table, axis=1)
predicted_fov_region = ...  # Define how to retrieve predicted fov region based on optimal_action
