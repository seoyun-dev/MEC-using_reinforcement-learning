import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import random

from Actor import Actor
from Critic import Critic
from Noise import OU_noise
from ReplayBuffer import ReplayBuffer


####### DDPG Agent 클래스

class DDPGAgent:
    def __init__(self, env):
        self.env             = env
        self.state_dim       = 5    # r1, r2, r3, W_M, W_U
        self.action_dim      = 2    # c,  prediction fov region

        self.OU              = OU_noise(self.action_dim)

        self.actor           = Actor(self.state_dim, self.action_dim)
        self.actor_target    = Actor(self.state_dim, self.action_dim)
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=1e-4)

        self.critic           = Critic(self.state_dim, self.action_dim)
        self.critic_target    = Critic(self.state_dim, self.action_dim)
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=5e-4)
        
        self.replay_buffer    = ReplayBuffer()  # 리플레이 버퍼
        self.batch_size       = 64              # 배치 사이즈  
        self.gamma            = 0.99            # 감쇠인자    
        self.tau              = 0.002           # soft target network update 파라미터

        self.update_target_models(tau=1)        # 타겟 파라미터들 초기화 (actor, critic과 같도록)


    ##### soft target 파라미터 업데이트 함수
    def update_target_models(self, tau=None):
        if tau is None:
            tau = self.tau
        # 타겟 파라미터 업데이트
        for target_param, param in zip(self.actor_target.parameters(), self.actor.parameters()):
            target_param.data.copy_(tau * param.data + (1 - tau) * target_param.data)
        for target_param, param in zip(self.critic_target.parameters(), self.critic.parameters()):
            target_param.data.copy_(tau * param.data + (1 - tau) * target_param.data)


    ##### 학습(업데이트) 진행 함수 
    def train(self):
        if len(self.memory) < self.batch_size:
            return

        state, next_state, action, reward, done = self.replay_buffer.sample(self.batch_size)
        state       = torch.Tensor(state, dtype=torch.float32)
        next_state  = torch.Tensor(next_state, dtype=torch.float32)
        action      = torch.Tensor(action, dtype=torch.float32)
        reward      = torch.Tensor(reward, dtype=torch.float32)
        done        = torch.Tensor(done, dtype=torch.float32)

        ### Critic 업데이트
        # 타겟 Q값 구하기
        future_Q = self.critic_target(next_state, self.actor_target(next_state)) 
        target_Q = reward + ((1 - done) * self.gamma * future_Q).detach()     # 타겟 Q값 계산
        current_Q =self.critic(state, action)
        # critic 파라미터 손실 계산 및 역전파
        critic_loss = F.mse_loss(current_Q, target_Q)
        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()

        ### Actor 업데이트
        actor_loss = -self.critic(state, self.actor(state)).mean() # 정책의 목적함수는 정책함수의 가치 > maximize해야 > - 붙임
        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()

        ### actor, critic 파라미터 업데이트
        self.update_target_models()


    ##### 메인 루프 함수
    def run(self, max_episodes=1000):
        for ep in range(max_episodes):
            state          = self.env.reset()
            episode_reward = 0
            done           = False

            # TODO 왜지.. done이 True가 나오지 않으므로 안끝남; 
            # while not done:
            for _ in range(200):
                self.env.render()
                # # state 전처리
                # if type(state) == tuple:
                #     # state를 튜플 내의 배열로부터 가져옴
                #     state_array = state[0]
                #     # 배열 내의 요소들을 가져와서 처리
                #     value_1 = state_array[0]    # state
                #     value_2 = state_array[1]    # action    
                #     value_3 = state_array[2]    # reward
                #     # 가져온 값들을 원하는 형태로 처리 (예: numpy 배열로 변환)
                #     state   = np.array([value_1, value_2, value_3], dtype=np.float32)
                # state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)

                # action 선택 (by actor, noise)
                action = self.actor(state).squeeze(0).detach().numpy()
                action = action + self.OU.sample()
                next_state, reward,done, a, b = self.env.step(action)

                # 한 transition 데이터 저장
                self.replay_buffer.remember(state, action, reward, next_state, done)
                episode_reward += reward
                state           = next_state

                if len(self.replay_buffer) > self.batch_size:
                    self.train()

                if done:
                    break

            # 200 trans마다 출력
            print(f"200 trans: {ep + 1}, Reward: {episode_reward}")

        self.env.close()