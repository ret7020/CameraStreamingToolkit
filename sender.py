import socket
import cv2
from s_config import *

try:
    cap = cv2.VideoCapture(0)


    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP

    while True:
        ret, img = cap.read()
        img = cv2.resize(img, (0, 0), fx=0.7, fy=0.7)
        if ret:
            img_bytes = cv2.imencode('.jpg', img)[1].tobytes()
            sock.sendto(img_bytes, (UDP_IP, UDP_PORT))

except KeyboardInterrupt:
    cap.release()
    exit()
