import cv2
import logging
from shared_memory_dict import SharedMemoryDict
import numpy as np
import openfb.resources.function_blocks.openCV.CVsettings as CVsettings

class CornerHarris():
    def __init__(self):
        self.smd_connections = {}
        self.buffer_size = CVsettings.IMAGE_BUFFER_SIZE * CVsettings.IMAGE_HEIGHT * CVsettings.IMAGE_WIDTH * CVsettings.IMAGE_CHANNELS

    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, BLOCK_SIZE, KSIZE, K, BORDERTYPE):
        if event_input_name == 'REQ':
            if QUEUE_ID not in self.smd_connections:
                self.smd_connections[QUEUE_ID] = SharedMemoryDict(name=QUEUE_ID, size=self.buffer_size)
            self.smd = self.smd_connections[QUEUE_ID]
            img_key = str(IMG_ID)
            data = self.smd.get(img_key)
            if data is not None:
                img = data['image']
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray = np.float32(gray)
                dst = cv2.cornerHarris(gray, int(BLOCK_SIZE), int(KSIZE), K, borderType=BORDERTYPE)
                dst = cv2.dilate(dst, None)
                img[dst > 0.01 * dst.max()] = [0, 0, 255]
                data['image'] = img
                self.smd[img_key] = data
                return event_input_value, IMG_ID

    def __del__(self):
        logging.info("Delete CornerHarris")
        for smd in self.smd_connections.values():
            del smd