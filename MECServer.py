from PredictionFov import PredictionFov

class MECServer:
    def __init__(self, W_M, R2):
        self.packet_buffer               = None
        self.saliency_map                = None
        self.fov_prediction_distribution = PredictionFov()
        self.computation_performance     = W_M
        self.transmission_rate           = R2

    def transmit_data_to_user(self,data):
        # 사용자에게 데이터를 전송
        delay = data / self.transmission_rate  # 10*(0,160)Mbps
        return delay
    
    def caching_transmit(self, data):
        delay = data 

    def get_predict_fov(self):
        # FOV 예측 분포를 생성
        return self.fov_prediction_distribution.getFov()

    def offload_computation(self, data):
        # 데이터 처리 로직을 GPU로 오프로딩
        delay = data / self.computation_performance
        return delay