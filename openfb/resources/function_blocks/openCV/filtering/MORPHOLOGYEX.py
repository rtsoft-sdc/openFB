import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class MORPHOLOGYEX():
        
    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, MORPH_OP, KERNEL):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.get(queue_id=QUEUE_ID, img_id=IMG_ID)
            
            if img is not None:
                img = cv2.morphologyEx(img, MORPH_OP, KERNEL, dst=img)
                return event_input_value, "OK", IMG_ID
            return event_input_value, "ERROR: no image found", None

    def __del__(self):
        pass