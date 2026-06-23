import cv2
import logging
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory


class Blur():
        
    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, KSIZE, ANCHOR):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.pop(queue_id=QUEUE_ID, img_id=IMG_ID)
            
            if img is not None:
                cv2.blur(img, (int(KSIZE[0]), int(KSIZE[1])), dst=img, anchor=(int(ANCHOR[0]), int(ANCHOR[1])), borderType=cv2.BORDER_DEFAULT)
                return event_input_value, IMG_ID, QUEUE_ID, "OK"        
            logging.error(f"Image with ID {IMG_ID} not found in shared memory for QUEUE_ID {QUEUE_ID}.")
            return event_input_value, None, None, "ERROR: Image not found"

    def __del__(self):
        logging.info("Delete Blur")