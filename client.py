import socket
import numpy as np
import cv2
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
last_img_time = 0
while True:
    data, addr = sock.recvfrom(102400) # buffer size is 1024 bytes
    nparr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(nparr, 3)
    curr_time = time.time()
    print("FPS:", 1 / (curr_time - last_img_time))
    last_img_time = curr_time
    print(img.shape)
    cv2.imshow("From Server", img)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
