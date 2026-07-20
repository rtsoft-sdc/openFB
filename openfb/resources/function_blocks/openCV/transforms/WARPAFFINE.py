import cv2
import numpy as np
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class WARPAFFINE:

    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, TRANSFORMATION_MATRIX, DSIZE):
        if event_input_name == 'REQ':
            queue_id = GlobalVideoMemory.get_queue_id(QUEUE_ID)
            img = GlobalVideoMemory.get(queue_id=queue_id, img_id=IMG_ID)
            if img is not None:
                try:
                    mat = np.array(TRANSFORMATION_MATRIX, dtype=np.float32).reshape(2, 3)
                    dsize = (DSIZE[0], DSIZE[1])
                    img = cv2.warpAffine(img, mat, dsize)
                    GlobalVideoMemory.set(queue_id=queue_id, img_id=IMG_ID, frame=img)
                    return event_input_value, "OK", IMG_ID
                except Exception as e:
                    return event_input_value, f"ERROR: {e}", None

            return event_input_value, "ERROR: Image not found", None

    def __del__(self):
        pass