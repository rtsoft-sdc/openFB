import cv2
import logging
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class Resize():

    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, WIDTH, HEIGHT, INTERPOLATION):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.pop(QUEUE_ID, IMG_ID)
            if img is not None:
                img = cv2.resize(img, (WIDTH, HEIGHT), interpolation=INTERPOLATION)
                GlobalVideoMemory.push(QUEUE_ID, IMG_ID, img)
                return event_input_value, IMG_ID, QUEUE_ID, "OK"
            
            logging.error(f"Image with ID {IMG_ID} not found in queue {QUEUE_ID}.")
            return event_input_value, IMG_ID, QUEUE_ID, "Image not found"

    def __del__(self):
        logging.info("Delete Resize")
