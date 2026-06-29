import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class THRESHOLD():
    
    def get_opencv_thresh_param(self, param_number: int) -> int:
        if param_number == 0:
            return cv2.THRESH_BINARY_INV
        if param_number == 1:
            return cv2.THRESH_BINARY
        if param_number == 2:
            return cv2.THRESH_TOZERO_INV
        if param_number == 3:
            return cv2.THRESH_TOZERO
        if param_number == 4:
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