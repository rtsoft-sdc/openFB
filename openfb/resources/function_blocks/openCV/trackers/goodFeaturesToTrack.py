import cv2
import logging
from openfb.resources.function_blocks.openCV import CVsettings
from shared_memory_dict import SharedMemoryDict
import numpy as np

class GoodFeaturesToTrack():
    def __init__(self):
        self.smd_connections = {}
        self.buffer_size = CVsettings.IMAGE_BUFFER_SIZE * CVsettings.IMAGE_HEIGHT * CVsettings.IMAGE_WIDTH * CVsettings.IMAGE_CHANNELS
        
    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, MAXCORNERS, QUALITYLEVEL, MINDISTANCE, MASK, CORNERSQUALITY, BLOCK_SIZE, GRADIENTSIZE, USE_HARRIS, K):
        if event_input_name == 'REQ':
            if QUEUE_ID not in self.smd_connections:
                self.smd_connections[QUEUE_ID] = SharedMemoryDict(name=QUEUE_ID, size=self.buffer_size)
            self.smd = self.smd_connections[QUEUE_ID]
            img_key = str(IMG_ID)
            data = self.smd.get(img_key)
            if data is not None:
                img = data['image']
                corners = cv2.goodFeaturesToTrack(img, MAXCORNERS, QUALITYLEVEL, MINDISTANCE, mask=MASK, blockSize=BLOCK_SIZE, gradientSize=GRADIENTSIZE, useHarrisDetector=USE_HARRIS, k=K)
                corners_quality = corners[:, 0, 1].tolist() if corners is not None else []
                return event_input_value, IMG_ID, corners_quality

    def __del__(self):
        logging.info("Delete GoodFeaturesToTrack")
        for smd in self.smd_connections.values():
            del smd