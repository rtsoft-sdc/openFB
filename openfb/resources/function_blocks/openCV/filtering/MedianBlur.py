import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory
class MedianBlur():
        
    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, KSIZE):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.pop(queue_id=QUEUE_ID, img_id=IMG_ID)
            
            if img is not None:
                img = cv2.MedianBlur(img, ksize=(KSIZE[0], KSIZE[1]), dst=img)
                return event_input_value, "OK", IMG_ID
            return event_input_value, "ERROR: no image found", None

    def __del__(self):
        pass