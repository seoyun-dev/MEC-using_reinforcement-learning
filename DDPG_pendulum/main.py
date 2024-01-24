from DDPGAgent import DDPGAgent
from Env import VRStreamingEnv

if __name__ == "__main__":
    # env   = gym.make('Pendulum-v1', render_mode="rgb_array")
    agent = DDPGAgent(VRStreamingEnv)
    agent.run()