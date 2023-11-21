import websocket
import gzip
import numpy as np
import cv2
from multiprocessing import Process


def on_message(ws, message):
    payload = gzip.decompress(message)
    nparr = np.frombuffer(payload, np.byte)
    image = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)
    print("Got frame")

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("Closed connection")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("ws://localhost:5000/image/fhd",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()
    