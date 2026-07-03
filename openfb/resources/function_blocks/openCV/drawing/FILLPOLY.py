import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory
import numpy as np

#check arraysofarrays - add input

class FILLPOLY():
        
    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, POINTCOUNT, POINTS, COLOR):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.get(queue_id=QUEUE_ID, img_id=IMG_ID)

            if img is not None:
                cv2.fillPoly(img, [np.array(POINTS[:POINTCOUNT], dtype=np.int32)], (int(COLOR[0]), int(COLOR[1]), int(COLOR[2])))
                return event_input_value, "OK", IMG_ID
            return event_input_value, "ERROR: Image not found", None


    def __del__(self):
        pass