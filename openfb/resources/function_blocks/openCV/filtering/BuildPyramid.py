import cv2
import logging
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class BuildPyramid():
        
    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, MAXLEVEL):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.pop(queue_id=QUEUE_ID, img_id=IMG_ID)
            if img is not None:
                pyramid_list = cv2.buildPyramid(img, MAXLEVEL, borderType=cv2.BORDER_DEFAULT)
                GlobalVideoMemory.push(queue_id=QUEUE_ID, img_id=IMG_ID, img=pyramid_list)
                return event_input_value, IMG_ID, QUEUE_ID, 'OK'
            logging.error(f"Failed to retrieve image with ID {IMG_ID} from shared memory queue {QUEUE_ID}")
            return event_input_value, None, None, "ERROR: Image not found"

    def __del__(self):
        logging.info("Delete BuildPyramid")
        for smd in self.smd_connections.values():
            del smd