from PredictionFov import PredictionFov
import random

class MECServer:
    def __init__(self):
        self.packet_buffer = None
        self.gpu = None
        self.saliency_map = None
        self.fov_prediction_distribution = PredictionFov()

    def transmit_data_to_user(self,data):
        # 사용자에게 데이터를 전송합니다.
        delay=data/(10*random.randint(0,160000000)) #10*(0,160)Mbps
        return delay

    def get_predict_fov(self):
        # FOV 예측 분포를 생성합니다. (더미 함수)
        return self.fov_prediction_distribution.getFov()

    def offload_computation(self, data):
        W_M = 1.6 * (10**12)  # MEC 서버에서 초당 처리되는 데이터 크기
        # 데이터 처리 로직을 GPU로 오프로딩합니다.
        delay=data/W_M
        return delay
