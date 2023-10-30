from PredictionFov import PredictionFov
import random

class MECServer:
    def __init__(self):
        self.packet_buffer = None
        self.gpu = None
        self.saliency_map = None
        self.fov_prediction_distribution = PredictionFov()

    # def receive_data_from_cloud_server(self, data):
    #     # 클라우드 서버로부터 데이터를 수신합니다.
    #     self.packet_buffer = data

    # def decode_data(self):
    #     # 데이터 디코딩을 수행합니다. (더미 함수)
    #     decoded_data = self.decode(self.packet_buffer)
    #     return decoded_data

    # def offload_computation_to_gpu(self, data):
    #     # 데이터 처리를 GPU로 오프로딩합니다. (더미 함수)
    #     processed_data = self.offload_computation(data)
    #     return processed_data

    def transmit_data_to_user(self,data):
        # 사용자에게 데이터를 전송합니다.
        delay=data/(10*random.randint(0,160000000)) #10*(0,160)Mbps
        return delay

    def transmit_data_to_cloud_server(self):
        # 클라우드 서버로 데이터를 전송합니다.
        return self.packet_buffer

    # def generate_saliency_map(self, video_data):
    #     # 쎌리언시 맵을 생성합니다. (더미 함수)
    #     saliency_map = self.generate_saliency_map(video_data)
    #     self.saliency_map = saliency_map

    def get_predict_fov(self):
        # FOV 예측 분포를 생성합니다. (더미 함수)
        return self.fov_prediction_distribution.getFov()

    def decode(self, data):
        # 데이터 디코딩 로직을 구현합니다.
        return "Decoded Data"

    def offload_computation(self, data):
        W_M = 1.6 * (10**12)  # MEC 서버에서 초당 처리되는 데이터 크기
        # 데이터 처리 로직을 GPU로 오프로딩합니다.
        delay=data/W_M
        return delay
