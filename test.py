import numpy as np
import matplotlib.pyplot as plt
import random

from CloudServer import CloudServer
from VRUser import VRUser
from MECServer import MECServer

##################### 파라미터

# computation, 통신 관련 
s   = 1460       # UDP packet size (단위: bytes)
h   = 1.5        # computation 입력과 출력의 변화율
C_r = 1/600      # 비디오 청크의 압축률
D1  = 0.5        # Video chunk duration in seconds

# Video, frame 
fov_size = 1080 * 1200    # FoV의 1배율 사이즈 (가로*세로)
k = 1                     # 예측 FoV 비율
f = 60                    # fps (frames per second or the video chunk)
B  = 86.8                 # 1*1 사이즈의 프레임 당 데이터 크기(20Mbit/frame/.)

# E2E 임계치
D_th = 0.02      # seconds

# 서버별 컴퓨팅 능력
W_M = 1.6 * (10**12)  # MEC 서버에서 초당 처리되는 데이터 크기
W_U = 1.6 * (40**9)   # User 에서 초당 처리되는 데이터 크기

# 강화학습 변동 파라미터
c  =0.99              # Offloading ratio of raw video data (MEC에서 캐시된 데이터들 중 c비율만 MEC에서 컴퓨팅)
R1 = random.randint(0,160000000)        # cloud > MEC 전송률
R2 = 10 * random.randint(0,160000000)   # MEC > user 전송률
R3 = random.randint(0,160000000)        # cloud > user 전송률



##################### 객체, 그래프 생성

cloudserver = CloudServer(R1, R3)      # 클라우드 서버
MECserver   = MECServer(W_M, R2)       # MEC 서버
vruser      = VRUser(W_U)              # VR 유저

plt.figure(figsize=(8, 6))
plt.grid(True)
plt.title("CDF of E2E Delay")
plt.xlabel("E2E Delay (ms)")
plt.ylabel("CDF")



##################### E2E delay 측정 위한 파라미터
eterate     = 1000
e2e_delays  = []
total_delay = 0
Fail        = 0

# E2E = D2+D3+D4+D5
for i in range(eterate):
    delay     = 0
    
    #D1 = MEC의 caching delay = cloud->MEC cacahing 통신 지연
    delay += fov_size * k**2 * C_r / R1
    #D2 = 예측과 실제 FoV 일치확인 지연 + 일치한 시야의 c 비율 랜더링 지연
    predictFov_rate  = MECserver.get_predict_fov()  # 예측 성공 비율
    delay += fov_size/W_M + fov_size*predictFov_rate*c/W_M

    #D3 = MEC > User 통신 지연
    delay += fov_size*predictFov_rate*(c*h + (1-c))*C_r/R2

    #D4 = Cloud > User 통신 지연
    delay += fov_size*(1-predictFov_rate)*C_r/R1 

    #D5 = HMD 계산 지연
    delay += ( fov_size*(1-predictFov_rate)+fov_size*predictFov_rate*(1-c) ) / W_U
        
    #딜레이 결과
    print("{} 번 실행 딜레이: {:.7f}초 (FoV예측 비율: {:.2f} %)".format(i+1, delay, 100*predictFov_rate))
    total_delay += delay
        
    if delay >= D_th: #임계치 제한 체크
        Fail   += 1
        
    # e2e_delays.append(delay * 1000) # E2E 값 저장
    e2e_delays.append(delay)
    

print("평균 딜레이: {:.5}초 (Fail: {}번)".format(total_delay/eterate, Fail))


sorted_delays = np.sort(e2e_delays)
y             = np.arange(1, len(sorted_delays)+1) / len(sorted_delays)

plt.plot(sorted_delays, y, marker='o')
plt.title("CDF of E2E Delay")
plt.xlabel("E2E Delay (ms)")
plt.ylabel("CDF")
plt.grid(True)
plt.show()
