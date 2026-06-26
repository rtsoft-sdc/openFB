import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory
class Erode():

    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, KERNEL, ITERATIONS):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.pop(queue_id=QUEUE_ID, img_id=IMG_ID)

            if img is not None:
                cv2.erode(img, KERNEL, dst=img, iterations=ITERATIONS)
                return event_input_value, "OK", IMG_ID
            return event_input_value, "ERROR: no image found", None

    def __del__(self):
        pass