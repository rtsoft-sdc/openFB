import cv2
import logging
from openfb.resources.function_blocks.openCV import CVsettings
from shared_memory_dict import SharedMemoryDict
import numpy as np

class ArucoDetector():
    def __init__(self):
        self.smd_connections = {}
        self.detector = None
        self.current_dict_id = None
        self.buffer_size = CVsettings.IMAGE_BUFFER_SIZE * CVsettings.IMAGE_HEIGHT * CVsettings.IMAGE_WIDTH * CVsettings.IMAGE_CHANNELS
        
    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, DICTIONARY):
        if event_input_name == 'REQ':
            if QUEUE_ID not in self.smd_connections:
                self.smd_connections[QUEUE_ID] = SharedMemoryDict(name=QUEUE_ID, size=self.buffer_size)
            smd = self.smd_connections[QUEUE_ID]
            img_key = str(IMG_ID)
            data = smd.get(img_key)
            if data is not None:
                img = data['image']
                if self.detector is None or self.current_dict_id != DICTIONARY:
                    self.detector = cv2.aruco.ArucoDetector(cv2.aruco.getPredefinedDictionary(DICTIONARY))
                    self.current_dict_id = DICTIONARY

                corners, ids, rejected = self.detector.detectMarkers(img)
                return event_input_value, IMG_ID, corners, ids, rejected

    def __del__(self):
        logging.info("Delete ArucoDetector")
        for smd in self.smd_connections.values():
            del self.smd