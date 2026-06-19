import cv2
import logging
from openfb.resources.function_blocks.openCV import CVsettings
from shared_memory_dict import SharedMemoryDict
import numpy as np

class MedianBlur():
    def __init__(self):
        self.smd_connections = {}
        self.buffer_size = CVsettings.IMAGE_BUFFER_SIZE * CVsettings.IMAGE_HEIGHT * CVsettings.IMAGE_WIDTH * CVsettings.IMAGE_CHANNELS        
        
    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, KSIZE):
        if event_input_name == 'REQ':
            if QUEUE_ID not in self.smd_connections:
                self.smd_connections[QUEUE_ID] = SharedMemoryDict(name=QUEUE_ID, size=self.buffer_size)
            smd = self.smd_connections[QUEUE_ID]
            img_key = str(IMG_ID)
            data = smd.get(img_key)
            if data is not None:
                img = data['image']
                img = cv2.MedianBlur(img, KSIZE, dst=img)
                smd[img_key] = data
                return event_input_value, IMG_ID

    def __del__(self):
        logging.info("Delete MedianBlur")
        for smd in self.smd_connections.values():
            del smd