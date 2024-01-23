from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import time
import cv2

def broadcast():
    while True:
        ret, img = app.camera.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        app.socketio.emit('img', cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 70])[1].tobytes())

app = Flask(__name__)
app.config['SECRET_KEY'] = 'passw'
app.socketio = SocketIO(app, async_mode='threading')
app.camera = cv2.VideoCapture(0)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.socketio.start_background_task(target=broadcast)
    app.socketio.run(app, port=8080, host="0.0.0.0")

