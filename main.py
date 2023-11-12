from flask import Flask, render_template
from flask_sock import Sock
import logging
import cv2
import numpy as np
# import threading
import time
import sys
import gzip
import base64

class Camera:
    def __init__(self, index) -> None:
        self.camera = cv2.VideoCapture(index)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
        self.image = cv2.imencode('.jpg', np.zeros((480, 640)), self.encode_params)[1].tobytes()
        logging.info("Camera inited")
        _, self.cache = self.camera.read()
        self.cache = cv2.cvtColor(self.cache, cv2.COLOR_BGR2GRAY)
        self.cache = cv2.imencode('.jpg', self.cache, self.encode_params)[1].tobytes()
        self.cache = gzip.compress(self.cache)
        

    def get_jpeg_image_bytes(self):
        #start_time = time.time()
        #_, img = self.camera.read()

        #print(1 / (time.time() - start_time))
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #res = cv2.imencode('.jpg', img, self.encode_params)[1].tobytes()
        #res = gzip.compress(res)
        
        return self.cache

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

sock = Sock(app)
camera = Camera("file_example_MP4_1920_18MG.mp4")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/control', methods=['POST'])
def api_manual_control():
    pass


@sock.route('/image')
def stream(sock):
    logging.error("Stream started")
    while True:
        sock.send(camera.get_jpeg_image_bytes())
        
