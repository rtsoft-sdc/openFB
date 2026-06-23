import cv2
import logging
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class Dilate():

    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, KERNEL, ANCHOR, ITERATIONS):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.pop(queue_id=QUEUE_ID, img_id=IMG_ID)
            
            if img is not None:
                cv2.dilate(src=img, dst=img, kernel=KERNEL, anchor=(ANCHOR[0], ANCHOR[1]), iterations=ITERATIONS)
                return event_input_value, IMG_ID, QUEUE_ID, 'OK'
            logging.error(f"Failed to retrieve image with ID {IMG_ID} from shared memory queue {QUEUE_ID}")
            return event_input_value, None, None, "ERROR: Image not found"

    def __del__(self):
        logging.info("Cleaning up Dilate resources")