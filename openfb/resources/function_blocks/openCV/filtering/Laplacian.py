import cv2
import logging
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory
class Laplacian():

    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, DDEPTH):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.pop(queue_id=QUEUE_ID, img_id=IMG_ID)
            
            if img is not None:
                img = cv2.Laplacian(img, DDEPTH, ksize=1, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT, dst=img)
                return event_input_value, IMG_ID, QUEUE_ID, 'OK'
            logging.error(f"Failed to retrieve image with ID {IMG_ID} from shared memory queue {QUEUE_ID}")
            return event_input_value, None, None, 'ERROR: no image found'

    def __del__(self):
        logging.info("Delete Laplacian")