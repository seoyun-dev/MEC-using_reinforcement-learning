import random
import numpy as np


# CNN + LSTM
# CNN 아키텍처: C32-C32-C32-C32-FC288 
# LSTM 네트워크: 10개의 비디오 프레임으로 구성된 비디오 프레임 슬라이딩 윈도우가 있다.
# 훈련 및 다른 네트워크 매개변수 설정에 대한 자세한 내용은 [31]을 참조하자.
class PredictionFov:
    def __init__(self):
        self.data = {
        "WaitingForLove": 0.7042685046323598,
        "SpaceWar"      : 0.5894272979827889,
        "KingKong"      : 0.540897356844711,
        "SpaceWar2"     : 0.6233880089121158,
        "Guitar"        : 0.6216974696171442,
        "BTSRun"        : 0.5312920575202599,
        "CMLauncher2"   : 0.6347282964835593,
        "Symphony"      : 0.669106020987788,
        "RioOlympics"   : 0.7695397332776495,
        "Dancing"       : 0.6590623821187533,
        "StarryPolar"   : 0.6511584747528362,
        "InsideCar"     : 0.7628155513781555,
        "Sunset"        : 0.7349986526376743,
        "Waterfall"     : 0.6883913118465134,
        "BlueWorld"     : 0.7158131732815242
        }
        self.values = list(self.data.values())
    
    def getFov(self):
        mean         = np.mean(self.values)
        std          = np.std(self.values)
        random_value = np.random.normal(mean, std)
        return random_value
    