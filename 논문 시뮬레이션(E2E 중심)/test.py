import numpy as np
import random
import time
import matplotlib.pyplot as plt
from CloudServer import CloudServer
from VRUser import VRUser
from MECServer import MECServer

##################### 파라미터

# computation, 통신 관련 
s   = 1460       # UDP packet size (단위: bytes)
h   = 1.5        # computation 입력과 출력의 변화율
C_r = 1/600      # 비디오 청크의 압축률
# TODO 이 설명이 맞는지 확인
c   = 0.99       # Offloading ratio of raw video data (MEC에서 캐시된 데이터들 중 c비율만 MEC에서 컴퓨팅)
D1  = 0.5        # Video chunk duration in seconds

# Video, frame 
M, N = 8, 4      # 투영된 비디오의 가로, 세로 타일 수

k = 2            # Fov당 타일의 수
f = 60           # fps (frames per second or the video chunk)
B  = 20000000    # 한 타일의 프레임 당 데이터 크기(20Mbit/frame/tile)

# E2E 임계치
D_th = 0.02      # seconds

# 서버별 컴퓨팅 능력
W_M = 1.6 * (10**12)  # MEC 서버에서 초당 처리되는 데이터 크기
W_U = 1.6 * (40**9)   # User 에서 초당 처리되는 데이터 크기



##################### 객체, 그래프 생성

cloudserver = CloudServer()     # 클라우드 서버
MECserver   = MECServer(W_M)    # MEC 서버
vruser      = VRUser(W_U)       # VR 유저

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
    total_bit = k**2 * B      # FoV 타일들의 비트 
        
    #D2 계산
    predictFov_rate  = MECserver.get_predict_fov()  # 예측 성공 비율
    delay           += MECserver.offload_computation(total_bit) # VR유저에게 받아온 실제 FOV와 예측 FOV비교
    # TODO 아래처럼 변경 맞는지 확인
    # 캐싱데이터 중 예측 성공한 데이터의 비율 c만큼 계산
    # delay           += MECserver.offload_computation((total_bit*predictFov_rate)*c) 

    #D3 계산
    delay += MECserver.transmit_data_to_user((total_bit*predictFov_rate)*C_r) # 예측 성공한 부분을 압축해 MEC 서버에서 VR 유저로 전송

    #D4 계산
    delay += cloudserver.transmit_data_to_user((total_bit*(1-predictFov_rate))*C_r) # 예측 실패한 부분을 압축해 클라우드 서버에서 VR 유저로 전송

    #D5 계산
    delay += vruser.offload_computation((total_bit*predictFov_rate)*(1-c)) # VR 유저에서 MEC가 오프로딩한 99%를 제외하고 계산
        
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
