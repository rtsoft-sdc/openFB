import cv2
import numpy as np
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class WarpPerspective:
        
    def schedule(
        self,
        event_input_name,
        event_input_value,
        QUEUE_ID,
        IMG_ID,
        TRANSFORMATION_MATRIX,
        DSIZE,
    ):
        if event_input_name == "REQ":
            img = GlobalVideoMemory.pop(QUEUE_ID, IMG_ID)
            if img is not None:
                try:
                    map = np.array(TRANSFORMATION_MATRIX, dtype=np.float32).reshape((3, 3))
                    dsize = (DSIZE[0], DSIZE[1])
                    img = cv2.warpPerspective(img, M=map, dsize=dsize)
                    GlobalVideoMemory.push(QUEUE_ID, IMG_ID, img)
                    return event_input_value, "OK", IMG_ID
                except Exception as e:
                    return event_input_value, "ERROR: Failed to warp perspective", None
            return event_input_value, "ERROR: Image not found", None

    def __del__(self):
        pass