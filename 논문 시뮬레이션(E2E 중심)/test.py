import numpy as np
import random
from CloudServer import CloudServer
from VRUser import VRUser
from MECServer import MECServer
# f = 60  # fps (frames per second)
# s = 1460  # UDP packet size
# h = 1.5  # Data size changing ratio after computation offloading
# C_r = 1/600  # Compression ratio of video chunk

# Video and frame parameters
k = 2  # Fov당 타일의 수
B = 20000000  # 프레임당 타일 데이터 크기(20Mbps)
c = 0.99  # Offloading ratio of raw video data
D1 = 0.5  # Video chunk duration in seconds

# E2E 임계치
D_th = 0.02  # seconds



cloudserver=CloudServer() #클라우드 서버
MECServer=MECServer() #MEC 서버
vruser=VRUser() #VR 유저

total_delay=0

# E2E = D2+D2+D4+D+5
for i in range(10): # 10번의 시뮬레이션 진행
    delay=0
    total_bit=k*B
    
    #D2 계산
    delay+=MECServer.offload_computation(total_bit) #VR유저에게 받아온 FOV와 예측 FOV비교
    predictFov_rate=MECServer.get_predict_fov() #예측 성공 비율

    #D3 계산
    delay+=MECServer.transmit_data_to_user(total_bit*predictFov_rate) #예측 성공한 부분을 MEC 서버에서 VR 유저에게 전송

    #D4 계산
    delay+=cloudserver.transmit_data_to_user(total_bit*(1-predictFov_rate)) #예측 실패한 부분을 클라우드 서버에서 VR 유저로 전송

    #D5 계산
    delay+=vruser.offload_computation((total_bit*predictFov_rate)*(1-c)) #VR 유저에서 MEC가 오프로딩한 99%를 제외하고 계산
    
    #딜레이 결과
    print("{} 번 실행 딜레이: {:.3f}초 (FoV예측 비율: {:.2f} %)".format(i+1,delay,100*predictFov_rate))
    total_delay+=delay
print("평균 딜레이: {:.5}초".format(total_delay/10))
