import cv2
import logging
from shared_memory_dict import SharedMemoryDict
import numpy as np

class CornerHarris():
    def __init__(self):
        self.smd = ""
        self.QUEUE_ID = ""
        
    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, BLOCK_SIZE, KSIZE, K, BORDERTYPE):
        if event_input_name == 'REQ':
            self.smd = SharedMemoryDict(name=QUEUE_ID, size=15*1080**2)
            if str(IMG_ID) in self.smd.keys():
                img = self.smd[str(IMG_ID)]
                corners = cv2.cornerHarris(img, BLOCK_SIZE, KSIZE, K, BORDERTYPE)
                self.smd[str(IMG_ID)] = img
                return event_input_value, IMG_ID

    def __del__(self):
        logging.info("Delete CornerHarris")
        self.smd.shm.unlink()
        self.smd.shm.close()
        del self.smd