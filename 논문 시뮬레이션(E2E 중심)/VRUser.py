class VRUser:
    def __init__(self, W_U):
        self.packet_buffer           = None
        # self.gpu                     = None   # TODO 이게 필요가 있나?
        # self.display                 = None   # TODO 이게 필요가 있나?
        self.motion_sensors          = None
        self.computation_performance = W_U

    def offload_computation(self, data):
        # 데이터 처리 로직을 GPU로 오프로딩합니다.
        delay = data / self.computation_performance
        return delay 

