import cv2

IMAGE_HEIGHT = 1080
IMAGE_WIDTH = 1920
IMAGE_CHANNELS = 3
IMAGE_BUFFER_SIZE = 5

def get_opencv_thresh_param(param_name: str) -> int:
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
    
def get_opencv_adaptive_method_param(param_name: str) -> int:
    clean_name = param_name.strip().lower()
    if 'mean' in clean_name:
        return cv2.ADAPTIVE_THRESH_MEAN_C
    if 'gaussian' in clean_name:
        return cv2.ADAPTIVE_THRESH_GAUSSIAN_C