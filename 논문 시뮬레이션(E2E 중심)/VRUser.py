class VRUser:
    def __init__(self):
        self.packet_buffer = None
        self.gpu = None
        self.display = None
        self.motion_sensors = None
        
    def offload_computation(self, data):
        W_U = 40 * (10**9)  # 사용자에서 초당 처리되는 데이터 크기 
        # 데이터 처리 로직을 GPU로 오프로딩합니다.
        delay=data/W_U
        return delay

