import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class BUILDPYRAMID():
        
    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, MAXLEVEL):
        if event_input_name == 'REQ':
            queue_id = GlobalVideoMemory.get_queue_id(QUEUE_ID)
            img = GlobalVideoMemory.get(queue_id=queue_id, img_id=IMG_ID)
            if img is not None:
                pyramid_list = cv2.buildPyramid(img, MAXLEVEL, borderType=cv2.BORDER_DEFAULT)
                GlobalVideoMemory.set(queue_id=queue_id, img_id=IMG_ID, frame=pyramid_list)
                return event_input_value, "OK", IMG_ID
            return event_input_value, "ERROR: Image not found", None

    def __del__(self):
        pass