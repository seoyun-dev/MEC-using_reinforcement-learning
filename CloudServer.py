import random

class CloudServer:
    def __init__(self):
        self.video_storage  = None
        self.selected_tiles = None

    def transmit_data_to_user(self,data):
        delay = data / random.randint(0,160000000) #(0,160)Mbps
        return delay
    
    def transmit_data_to_mec(self,data):
        delay = data / random.randint(0,160000000) #(0,160)Mbps
        return delay

