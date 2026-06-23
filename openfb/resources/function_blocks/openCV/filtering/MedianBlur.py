import cv2
import logging
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory
class MedianBlur():
        
    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, KSIZE):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.pop(queue_id=QUEUE_ID, img_id=IMG_ID)
            
            if img is not None:
                img = cv2.MedianBlur(img, ksize=(KSIZE[0], KSIZE[1]), dst=img)
                return event_input_value, IMG_ID, QUEUE_ID, 'OK'
            logging.error(f"Failed to retrieve image with ID {IMG_ID} from shared memory queue {QUEUE_ID}")
            return event_input_value, None, None, 'ERROR: no image found'

    def __del__(self):
        logging.info("Delete MedianBlur")