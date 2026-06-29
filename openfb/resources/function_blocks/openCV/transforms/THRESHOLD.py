import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class THRESHOLD():
    
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
        
    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, THRESH, MAX_VALUE, TYPE):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.get(QUEUE_ID, IMG_ID)
            if img is not None:
                thresh_value = self.get_opencv_thresh_param(TYPE)
                _, img = cv2.threshold(img, thresh_value, MAX_VALUE, TYPE)
                GlobalVideoMemory.set(QUEUE_ID, IMG_ID, img)
                return event_input_value, "OK", IMG_ID
            
            return event_input_value, "ERROR: Image not found", IMG_ID

    def __del__(self):
        pass