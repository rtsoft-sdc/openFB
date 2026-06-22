import cv2
import logging
from openfb.resources.function_blocks.openCV import CVsettings
from shared_memory_dict import SharedMemoryDict

class AdaptiveThreshold():
    def __init__(self):
        self.smd_connections = {}
        self.buffer_size = CVsettings.IMAGE_BUFFER_SIZE * CVsettings.IMAGE_HEIGHT * CVsettings.IMAGE_WIDTH * CVsettings.IMAGE_CHANNELS


    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, MAX_VALUE, ADAPTIVE_METHOD, THRESHOLD_TYPE, BLOCK_SIZE, C):
        if event_input_name == 'REQ':
            if QUEUE_ID not in self.smd_connections:
                self.smd_connections[QUEUE_ID] = SharedMemoryDict(name=QUEUE_ID, size=self.buffer_size)
            smd = self.smd_connections[QUEUE_ID]
            img_key = str(IMG_ID)
            data = smd.get(img_key)
            if data is not None:
                img = data['image']
                if len(img.shape) == 3 and img.shape[2] == 3:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                if(BLOCK_SIZE % 2 == 0):
                    block_size += 1
                adaptive_method = CVsettings.get_opencv_adaptive_method_param(ADAPTIVE_METHOD)
                threshold_type = CVsettings.get_opencv_thresh_param(THRESHOLD_TYPE)
                img = cv2.adaptiveThreshold(img, MAX_VALUE, adaptive_method, threshold_type, block_size, C, dst=img)
                data['image'] = img
                smd[img_key] = data
                return event_input_value, IMG_ID
            
    def __del__(self):
        logging.info("Delete Adaptive Threshold")
        for smd in self.smd_connections.values():
            del smd