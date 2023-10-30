import random

class CloudServer:
    def __init__(self):
        self.video_storage = None
        self.selected_tiles = None

    # def receive_video_data(self, video_data):
    #     # 비디오 데이터를 받아 저장합니다.
    #     self.video_storage = video_data

    # def tile_encoding_and_compressing(self, video_data):
    #     # 비디오 데이터를 타일로 인코딩 및 압축합니다. (더미 함수)
    #     encoded_data = self.encode_and_compress(video_data)
    #     return encoded_data

    # def saliency_map_network(self, video_data):
    #     # 비디오 데이터를 사용하여 쎌리언시 맵을 생성합니다. (더미 함수)
    #     saliency_map = self.generate_saliency_map(video_data)
    #     return saliency_map

    # def tile_selection(self, saliency_map):
    #     # 쎌리언시 맵을 기반으로 타일 선택을 수행합니다. (더미 함수)
    #     selected_tiles = self.select_tiles(saliency_map)
    #     self.selected_tiles = selected_tiles

    def transmit_data_to_mec_server(self):
        # MEC 서버로 데이터를 전송합니다.
        return self.selected_tiles

    def transmit_data_to_user(self,data):
        delay=data/random.randint(0,160000000) #(0,160)Mbps
        return delay

    def encode_and_compress(self, video_data):
        # 비디오 데이터를 인코딩하고 압축하는 로직을 구현해야 합니다.
        # 실제 비디오 처리 알고리즘에 따라 함수를 작성합니다.
        # 더미 함수로 구현합니다.
        return "Encoded and Compressed Data"

    # def generate_saliency_map(self, video_data):
    #     # 쎌리언시 맵을 생성하는 로직을 구현해야 합니다.
    #     # 실제 쎌리언시 맵 생성 알고리즘에 따라 함수를 작성합니다.
    #     # 더미 함수로 구현합니다.
    #     return "Saliency Map"

    # def select_tiles(self, saliency_map):
    #     # 쎌리언시 맵을 기반으로 타일 선택을 수행하는 로직을 구현해야 합니다.
    #     # 실제 타일 선택 알고리즘에 따라 함수를 작성합니다.
    #     # 더미 함수로 구현합니다.
    #     return "Selected Tiles"
