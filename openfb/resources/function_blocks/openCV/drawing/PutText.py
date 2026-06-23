import cv2
import logging
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory
class PutText():
        
    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, ORG, TEXT, FONT_FACE, FONT_SCALE, COLOR, THICKNESS, BOTTOMLEFTORIGIN):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.pop(queue_id=QUEUE_ID, img_id=IMG_ID)

            if img is not None:
                cv2.putText(img, TEXT, (int(ORG[0]), int(ORG[1])), FONT_FACE, FONT_SCALE, (int(COLOR[0]), int(COLOR[1]), int(COLOR[2])), THICKNESS, BOTTOMLEFTORIGIN)
                return event_input_value, IMG_ID, QUEUE_ID, "OK"
            logging.error(f"Image with ID {IMG_ID} not found in shared memory for QUEUE_ID {QUEUE_ID}.")
            return event_input_value, None, None, "ERROR: Image not found"
        
    def __del__(self):
        logging.info("Delete PutText")