import torch
import torch.nn as nn


# Actor 신경망 
# [입력] state : 통신 상태 (R1, R2, R3), 계산 효율 (W_M, W_U)
# [출력] action : c(0~1), k(비율/0.25,0.5,0.75,1)
class Actor(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(Actor, self).__init__()
        self.fc1 = nn.Linear(state_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 128)
        self.fc4 = nn.Linear(128, action_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = torch.sigmoid(self.fc4(x))    # c: 0~1
        if x[1] < 0.25 : x[1] = 0.25
        elif x[1] < 0.5 : x[1] = 0.5
        elif x[1] < 0.75 : x[1] = 0.75
        else : x[1] = 1

        return x