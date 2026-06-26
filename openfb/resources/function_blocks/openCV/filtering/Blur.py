import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory


class Blur():
        
    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, KSIZE):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.pop(queue_id=QUEUE_ID, img_id=IMG_ID)
            
            if img is not None:
                cv2.blur(img, (int(KSIZE[0]), int(KSIZE[1])), dst=img, borderType=cv2.BORDER_DEFAULT)
                return event_input_value, "OK", IMG_ID
            return event_input_value, "ERROR: Image not found", None

    def __del__(self):
        pass