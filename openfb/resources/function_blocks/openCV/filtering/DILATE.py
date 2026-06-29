import cv2
import numpy as np
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class DILATE():

    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, KERNEL, ITERATIONS):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.get(queue_id=QUEUE_ID, img_id=IMG_ID)
            kernel = np.array(KERNEL, dtype=np.uint8).reshape((int(np.sqrt(len(KERNEL))), int(np.sqrt(len(KERNEL)))))
            if img is not None:
                cv2.dilate(src=img, dst=img, kernel=kernel, iterations=ITERATIONS)
                return event_input_value, "OK", IMG_ID
            return event_input_value, "ERROR: Image not found", None

    def __del__(self):
        pass