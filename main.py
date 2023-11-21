from flask import Flask, render_template
from flask_sock import Sock
import logging
import cv2
import numpy as np
import gzip
from multiprocessing import Process, Queue

class Camera:
    def __init__(self, index) -> None:
        self.camera = cv2.VideoCapture(index)
        # self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        # self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
        self.image = cv2.imencode('.jpg', np.zeros((480, 640)), self.encode_params)[1].tobytes() # Fallback image
        self.image = gzip.compress(self.image)
        logging.info("Camera inited")

    def get_jpeg_image_bytes(self):
        #start_time = time.time()
        _, img = self.camera.read()

        #print(1 / (time.time() - start_time))

        # local_share_img = cv2.resize(img, (1080, 1080))
        web_share_img = img.copy()
        web_share_img = cv2.cvtColor(web_share_img, cv2.COLOR_BGR2GRAY)
        web_share_img = cv2.resize(web_share_img, (640, 480))
        web_share_img = cv2.imencode('.jpg', web_share_img, self.encode_params)[1].tobytes()
        web_share_img = gzip.compress(web_share_img)

        local_share_img = cv2.resize(img, (1920, 1080))
        local_share_img = cv2.imencode('.jpg', local_share_img, self.encode_params)[1].tobytes()
        local_share_img = gzip.compress(local_share_img)
        
        return local_share_img, web_share_img
    
    def loop(self, image_local_share, image_web_share):
        while True:
            local_share_img, web_share_img = self.get_jpeg_image_bytes()
            image_local_share.put(local_share_img)
            image_web_share.put(web_share_img)

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

sock = Sock(app)
camera = Camera(0)
image_local_share = Queue()
image_web_share = Queue()
p = Process(target=camera.loop, args=(image_local_share, image_web_share, ))
p.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stop')
def stop_api():
    p.terminate()
    return "1"

@sock.route('/image/sd')
def stream_sd_resolution(sock):
    logging.error("SD Stream started")
    while True:
        sock.send(image_web_share.get())

@sock.route('/image/fhd')
def stream_fhd_resolution(sock):
    logging.error("FHD Stream started")
    while True:
        sock.send(image_local_share.get())