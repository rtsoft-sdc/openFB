import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class ADAPTIVETHRESHOLD():

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
        
    def get_opencv_adaptive_method_param(self, param_number: int) -> int:
        if param_number == 0:
            return cv2.ADAPTIVE_THRESH_MEAN_C
        if param_number == 1:
            return cv2.ADAPTIVE_THRESH_GAUSSIAN_C

    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, MAX_VALUE, ADAPTIVE_METHOD, THRESHOLD_TYPE, BLOCK_SIZE, C):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.get(QUEUE_ID, IMG_ID)
            if img is not None:
                if len(img.shape) == 3 and img.shape[2] == 3:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                block_size = BLOCK_SIZE
                if(BLOCK_SIZE % 2 == 0):
                    block_size += 1
                if BLOCK_SIZE < 3:
                    block_size = 3
                    
                adaptive_method = self.get_opencv_adaptive_method_param(ADAPTIVE_METHOD)
                threshold_type = self.get_opencv_thresh_param(THRESHOLD_TYPE)

                img = cv2.adaptiveThreshold(img, MAX_VALUE, adaptive_method, threshold_type, block_size, C, dst=img)
                GlobalVideoMemory.set(QUEUE_ID, IMG_ID, img)

                return event_input_value, "OK", IMG_ID
            return event_input_value, "ERROR: Image not found", IMG_ID

    def __del__(self):
        pass