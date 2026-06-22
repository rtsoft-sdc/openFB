import cv2
import logging
from openfb.resources.function_blocks.openCV import CVsettings
from openfb.resources.function_blocks.openCV.videoMemoryDict import VideoSharedMemory

class Rectangle():
    def __init__(self):
        self.buffer_size = CVsettings.BUFFER_SIZE
        self.smd = None
        self.queue_id = None
        
    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, PT1, PT2, COLOR, THICKNESS):
        if event_input_name == 'REQ':
            if QUEUE_ID != self.queue_id:
                self.smd = VideoSharedMemory(name=QUEUE_ID, size=self.buffer_size)
                self.queue_id = QUEUE_ID
            img = self.smd.get_frame(int(IMG_ID))
            
            if img is not None:
                cv2.rectangle(img, (int(PT1[0]), int(PT1[1])), (int(PT2[0]), int(PT2[1])), (int(COLOR[0]), int(COLOR[1]), int(COLOR[2])), int(THICKNESS), dst=img)
                return event_input_value, IMG_ID, QUEUE_ID, "OK"
            logging.error(f"Image with ID {IMG_ID} not found in shared memory for QUEUE_ID {QUEUE_ID}.")
            return event_input_value, None, None, "ERROR: Image not found"
            
    def __del__(self):
        logging.info("Delete Rectangle")