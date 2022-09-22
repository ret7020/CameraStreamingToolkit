import socket
import numpy as np
import cv2
import time
from c_config import *


class Client:
    def __init__(self, server_ip, server_port, buffer_size, count_fps=True):
        self.sock = socket.socket(socket.AF_INET,
                socket.SOCK_DGRAM) # UDP
        self.sock.bind((server_ip, server_port))
        self.buffer_size = buffer_size
        self.count_fps = count_fps
        if self.count_fps:
            self.last_img_time = 0
            

    def stream_loop(self):
        while True:
            data, addr = self.sock.recvfrom(self.buffer_size)
            nparr = np.frombuffer(data, np.uint8)
            img = cv2.imdecode(nparr, 3)
            if self.count_fps:
                curr_time = time.time()
                print("FPS:", 1 / (curr_time - self.last_img_time))
                self.last_img_time = curr_time
            cv2.imshow("From Server", img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

if __name__ == "__main__":
    client = Client(UDP_IP, UDP_PORT, BUFFER_SIZE)
    client.stream_loop()    
