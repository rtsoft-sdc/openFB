import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class MORPHOLOGYEX():
    
    def get_morphology_operation(self, operation_name):
        operation_name = operation_name.upper()
        operations = {
            "ERODE": cv2.MORPH_ERODE,
            "DILATE": cv2.MORPH_DILATE,
            "OPEN": cv2.MORPH_OPEN,
            "CLOSE": cv2.MORPH_CLOSE,
            "GRADIENT": cv2.MORPH_GRADIENT,
            "TOPHAT": cv2.MORPH_TOPHAT,
            "BLACKHAT": cv2.MORPH_BLACKHAT
        }
        return operations.get(operation_name, None)
        
    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, MORPH_OP, KERNEL):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.get(queue_id=QUEUE_ID, img_id=IMG_ID)
            morph_op = self.get_morphology_operation(MORPH_OP)
            if img is not None:
                img = cv2.morphologyEx(img, morph_op, KERNEL, dst=img)
                return event_input_value, "OK", IMG_ID
            return event_input_value, "ERROR: no image found", None

    def __del__(self):
        pass