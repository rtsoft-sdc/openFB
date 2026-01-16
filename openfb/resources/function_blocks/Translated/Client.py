from time import sleep
import time
from shared_memory_dict import SharedMemoryDict
import cv2
import socket
import struct
import pickle
import logging


class Client:
    def __init__(self) -> None:
        self.smd = ""
        image_shape = 1080  # max width, height parametr
        container_size = 15  # number of images that could be stored
        self.max_size = container_size*image_shape**2
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isConnection_created = False
        self.last = 0
        self.current = 0

    def __del__(self):
        self.client_socket.close()

    def schedule(self, event_input_name, event_input_value, QI, IMG_ID, Compress_level, QUEUE_ID, IP, Port):
        'Write your code here.'
        if event_input_name == 'INIT':
            "Write your handler for current event here."
            logging.error("Connect to IP: %s", IP)
            sleep(1)
            self.smd = SharedMemoryDict(name=QUEUE_ID, size=self.max_size)
            if not self.isConnection_created:
                self.client_socket.connect((IP, int(Port)))
            self.isConnection_created = True
            self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), Compress_level]

            return event_input_value, 0, QI, None, "Inint done"
        if event_input_name == 'REQ':
            "Write your handler for current event here."
            if str(IMG_ID) in self.smd.keys():
                img = self.smd[str(IMG_ID)]["image"]
                img = cv2.resize(img, (640, 480))
                img = cv2.flip(img, 180)
                res, image = cv2.imencode('.jpg', img, self.encode_param)
                data = pickle.dumps(image, 0)
                size = len(data)
                self.client_socket.sendall(struct.pack(">L", size) + data)
                self.current = time.time()
                logging.error("Frame latency: %s" % (self.current - self.last))
                self.last = self.current
                return 0, event_input_value, QI, IMG_ID, "Image is sended to server"
            else:
                return 0, event_input_value, QI, -1, "Queue is disabled"
