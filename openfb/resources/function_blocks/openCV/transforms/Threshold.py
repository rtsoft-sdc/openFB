import cv2
import logging
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class Threshold():
    
    def get_opencv_thresh_param(self, param_name: str) -> int:
        clean_name = param_name.strip().lower()
        if 'binary_inv' in clean_name or 'inv' in clean_name and 'binary' in clean_name:
            return cv2.THRESH_BINARY_INV
        if 'binary' in clean_name:
            return cv2.THRESH_BINARY
        if 'tozero_inv' in clean_name or 'inv' in clean_name and 'tozero' in clean_name:
            return cv2.THRESH_TOZERO_INV
        if 'tozero' in clean_name:
            return cv2.THRESH_TOZERO
        if 'trunc' in clean_name:
            return cv2.THRESH_TRUNC
        
    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, THRESH, MAX_VALUE, TYPE):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.pop(QUEUE_ID, IMG_ID)
            if img is not None:
                thresh_value = self.get_opencv_thresh_param(TYPE)
                _, img = cv2.threshold(img, thresh_value, MAX_VALUE, TYPE)
                GlobalVideoMemory.push(QUEUE_ID, IMG_ID, img)
                return event_input_value, IMG_ID, QUEUE_ID, "OK"
            logging.error(f"Image with ID {IMG_ID} not found in queue {QUEUE_ID}.")
            return event_input_value, IMG_ID, QUEUE_ID, "Image not found"

    def __del__(self):
        logging.info("Delete Threshold")