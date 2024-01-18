class CloudServer:
    def __init__(self, R1, R3):
        self.video_storage             = None
        self.selected_tiles            = None
        self.transmission_rate_to_mec  = R1
        self.transmission_rate_to_user = R3

    def transmit_data_to_user(self,data):
        delay = data / self.transmission_rate_to_user #(0,160)Mbps
        return delay
    
    def transmit_data_to_mec(self,data):
        delay = data / self.transmission_rate_to_mec #(0,160)Mbps
        return delay