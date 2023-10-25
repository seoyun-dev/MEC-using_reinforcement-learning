import numpy as np

# Network transmission rate parameters
R_min = 0  # Mbps
R_max = 160  # Mbps

# Transmission rates from the cloud server to the MEC server and user
R1 = lambda t: np.random.uniform(R_min, R_max)  # R(t)
R2 = lambda t: 10 * np.random.uniform(R_min, R_max)  # 10 * R(t)
R3 = lambda t: np.random.uniform(R_min, R_max)  # R(t)

# Video and frame parameters
M, N = 8, 4  # Number of tiles in the vertical and horizontal directions in a projected video plane
k = 2  # Number of tiles in the FoV
f = 60  # fps (frames per second)
s = 1460  # UDP packet size
B = 20 * 1024 * 1024  # Data size per tile per frame in bits
W_M = 1.6 * 10**12  # Data size processed per second by the MEC server in bits per second
W_U = 40 * 10**9  # Data size processed per second by the user in bits per second
h = 1.5  # Data size changing ratio after computation offloading
c = 0.99  # Offloading ratio of raw video data
C_r = 1/600  # Compression ratio of video chunk
D1 = 0.5  # Video chunk duration in seconds

# Preset E2E delay threshold
D_th = 0.02  # seconds
