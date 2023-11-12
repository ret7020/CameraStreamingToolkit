import cv2
import time

cap = cv2.VideoCapture("file_example_MP4_1920_18MG.mp4")

while 1:
        start_time = time.time()
        ret, img = cap.read()
        print(1 / (time.time() - start_time))

