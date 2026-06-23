import cv2
import logging
import numpy as np
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class CornerHarris():

    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, BLOCK_SIZE, KSIZE, K, BORDERTYPE):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.pop(queue_id=QUEUE_ID, img_id=IMG_ID)
            if img is not None:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray = np.float32(gray)

                dst = cv2.cornerHarris(gray, int(BLOCK_SIZE), int(KSIZE), k=K, borderType=BORDERTYPE)
                dst = cv2.dilate(dst, None)
                img[dst > 0.01 * dst.max()] = [0, 0, 255]
                return event_input_value, IMG_ID

    def __del__(self):
        logging.info("Delete CornerHarris")