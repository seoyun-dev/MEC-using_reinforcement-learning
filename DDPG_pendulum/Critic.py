import torch
import torch.nn as nn


# Critic 신경망 정의
class Critic(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(Critic, self).__init__()
        self.fc1 = nn.Linear(state_dim+action_dim, 128)
        self.bn1 = nn.BatchNorm1d(128)  # 첫 번째 은닉층 후 배치 정규화
        self.fc2 = nn.Linear(128, 128)
        self.bn2 = nn.BatchNorm1d(128)  # 두 번째 은닉층 후 배치 정규화
        self.fc3 = nn.Linear(128, 128)
        self.bn3 = nn.BatchNorm1d(128)  # 세 번째 은닉층 후 배치 정규화
        self.fc4 = nn.Linear(128, action_dim)

    def forward(self, state, action):
        x     = torch.cat([state, action], 1)
        x     = torch.relu(self.bn1(self.fc1(x)))
        x     = torch.relu(self.bn2(self.fc2(x)))
        x     = torch.relu(self.bn3(self.fc3(x)))
        q_val = self.layer4(x)
        return q_val
    
        # x = self.layer1(state)

        # is_nested = any(isinstance(a_action, list) for a_action in action)

        # if not is_nested:
        #     # 단일 요소 리스트로 변환
        #     modified_list = [[a_action] for a_action in action]
        #     action_final_list = torch.cat([torch.tensor(a) for a in modified_list]).squeeze().unsqueeze(1)
        
        # x = torch.cat([x, action_final_list], dim=-1)

        # x = self.layer2(x)
        # x = self.layer3(x)
        # q_val = self.layer4(x)

        # return q_val