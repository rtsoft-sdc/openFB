import cv2
import logging
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory
class Scharr():
        
    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, DDEPTH, DX, DY):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.pop(queue_id=QUEUE_ID, img_id=IMG_ID)
            
            if img is not None:
                img = cv2.Scharr(img, DDEPTH, DX, DY, dst=img)
                return event_input_value, IMG_ID, QUEUE_ID, 'OK'
            logging.error(f"Failed to retrieve image with ID {IMG_ID} from shared memory queue {QUEUE_ID}")
            return event_input_value, None, None, 'ERROR'

    def __del__(self):
        logging.info("Delete Scharr")