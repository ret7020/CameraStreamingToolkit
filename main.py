from flask import Flask, render_template
from flask_sock import Sock
import logging
import cv2
import numpy as np
import time
import sys
import gzip
import base64
from multiprocessing import Process, Queue

class Camera:
    def __init__(self, index) -> None:
        self.camera = cv2.VideoCapture(index)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
        self.image = cv2.imencode('.jpg', np.zeros((480, 640)), self.encode_params)[1].tobytes()
        self.image = gzip.compress(self.image)
        logging.info("Camera inited")
        

    def get_jpeg_image_bytes(self):
        #start_time = time.time()
        _, img = self.camera.read()

        #print(1 / (time.time() - start_time))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        res = cv2.imencode('.jpg', img, self.encode_params)[1].tobytes()
        res = gzip.compress(res)
        
        return res
    
    def loop(self, image_share):
        while True:
            image_share.put(self.get_jpeg_image_bytes())

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

sock = Sock(app)
#camera = Camera("file_example_MP4_1920_18MG.mp4")
camera = Camera(0)
image_share = Queue()
p = Process(target=camera.loop, args=(image_share,))
p.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stop')
def stop_api():
    p.terminate()

@sock.route('/image')
def stream(sock):
    logging.error("Stream started")
    while True:
        sock.send(image_share.get())
        
