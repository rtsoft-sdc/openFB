import cv2
import logging
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class AdaptiveThreshold():

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
        
    def get_opencv_adaptive_method_param(self, param_name: str) -> int:
        clean_name = param_name.strip().lower()
        if 'mean' in clean_name:
            return cv2.ADAPTIVE_THRESH_MEAN_C
        if 'gaussian' in clean_name:
            return cv2.ADAPTIVE_THRESH_GAUSSIAN_C

    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, MAX_VALUE, ADAPTIVE_METHOD, THRESHOLD_TYPE, BLOCK_SIZE, C):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.pop(QUEUE_ID, IMG_ID)
            if img is not None:
                if len(img.shape) == 3 and img.shape[2] == 3:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                if(BLOCK_SIZE % 2 == 0):
                    block_size += 1
                if BLOCK_SIZE < 3:
                    block_size = 3
                    
                adaptive_method = self.get_opencv_adaptive_method_param(ADAPTIVE_METHOD)
                threshold_type = self.get_opencv_thresh_param(THRESHOLD_TYPE)

                img = cv2.adaptiveThreshold(img, MAX_VALUE, adaptive_method, threshold_type, block_size, C, dst=img)
                GlobalVideoMemory.push(QUEUE_ID, IMG_ID, img)

                return event_input_value, IMG_ID, QUEUE_ID, "OK"
            logging.error(f"Image with ID {IMG_ID} not found in queue {QUEUE_ID}.")
            return event_input_value, IMG_ID, QUEUE_ID, "Image not found"
            
            
    def __del__(self):
        logging.info("Delete Adaptive Threshold")