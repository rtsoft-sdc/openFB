import cv2
import logging
from openfb.resources.function_blocks.openCV import CVsettings
from openfb.resources.function_blocks.openCV.videoMemoryDict import VideoSharedMemory 
import numpy as np

class Dilate():
    def __init__(self):
        self.buffer_size = CVsettings.BUFFER_SIZE 
        self.smd = None
        self.queue_id = None

    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, KERNEL, ANCHOR, ITERATIONS, BORDER_TYPE, BORDERVALUE):
        if event_input_name == 'REQ':
            if QUEUE_ID != self.queue_id:
                self.smd = VideoSharedMemory(name=QUEUE_ID, size=self.buffer_size)
                self.queue_id = QUEUE_ID
            img = self.smd.get_frame(IMG_ID)
            
            if img is not None:
                cv2.dilate(src=img, dst=img, kernel=KERNEL, anchor=(ANCHOR[0], ANCHOR[1]), iterations=ITERATIONS, borderType=BORDER_TYPE, borderValue=BORDERVALUE)
                return event_input_value, IMG_ID, QUEUE_ID, 'OK'
            logging.error(f"Failed to retrieve image with ID {IMG_ID} from shared memory queue {QUEUE_ID}")
            return event_input_value, None, None, 'ERROR'
        
    def __del__(self):
        logging.info("Cleaning up Dilate resources")