import cv2
import numpy as np
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class MORPHOLOGYEX():
    
    def get_morphology_operation(self, operation_number):
        operations = {
            0: cv2.MORPH_ERODE,
            1: cv2.MORPH_DILATE,
            2: cv2.MORPH_OPEN,
            3: cv2.MORPH_CLOSE,
            4: cv2.MORPH_GRADIENT,
            5: cv2.MORPH_TOPHAT,
            6: cv2.MORPH_BLACKHAT
        }
        return operations.get(operation_number, None)

    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, KERNELSIZE, MORPH_OP, KERNEL):
        if event_input_name == 'REQ':
            queue_id = GlobalVideoMemory.get_queue_id(QUEUE_ID)
            img = GlobalVideoMemory.get(queue_id=queue_id, img_id=IMG_ID)
            morph_op = self.get_morphology_operation(MORPH_OP)
            kernel = np.array(KERNEL, dtype=np.uint8).reshape((KERNELSIZE, KERNELSIZE))
            if img is not None:
                img = cv2.morphologyEx(img, morph_op, kernel, dst=img)
                return event_input_value, "OK", IMG_ID
            return event_input_value, "ERROR: no image found", None

    def __del__(self):
        pass