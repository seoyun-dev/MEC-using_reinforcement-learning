import numpy as np
import random
from CloudServer import CloudServer
from VRUser import VRUser
from MECServer import MECServer

# Video and frame parameters
k = 2  # Fov당 타일의 수
B = 20000000  # 프레임당 타일 데이터 크기(20Mbps)
f = 60  # fps (frames per second)
s = 1460  # UDP packet size
h = 1.5  # Data size changing ratio after computation offloading
c = 0.99  # Offloading ratio of raw video data
C_r = 1/600  # Compression ratio of video chunk
D1 = 0.5  # Video chunk duration in seconds
# E2E 임계치
D_th = 0.02  # seconds



cloudserver=CloudServer()
MECServer=MECServer()
vruser=VRUser()

total_delay=0

for i in range(1): # 100번의 시뮬레이션 진행
    delay=0
    total_bit=k*B
    
    #D2 계산
    delay+=MECServer.offload_computation(total_bit)
    predictFov_rate=MECServer.get_predict_fov()

    #D3 계산
    delay+=MECServer.transmit_data_to_user(total_bit*predictFov_rate)

    #D4 계산
    delay+=cloudserver.transmit_data_to_user(total_bit*(1-predictFov_rate))

    #D5 계산
    delay+=vruser.offload_computation((total_bit*predictFov_rate)*(1-c))
    print(str(i) + "번 실행 딜레이: "+ str(delay))
    print(str(i) + "번 예측 FOV 비율: "+ str(predictFov_rate))
    total_delay+=delay
    
print("평균 딜레이: "+str(total_delay/10))
