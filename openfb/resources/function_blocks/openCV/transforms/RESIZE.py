import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class RESIZE():

    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, WIDTH, HEIGHT, INTERPOLATION):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.get(QUEUE_ID, IMG_ID)
            if img is not None:
                img = cv2.resize(img, (WIDTH, HEIGHT), interpolation=INTERPOLATION)
                GlobalVideoMemory.set(QUEUE_ID, IMG_ID, img)
                return event_input_value, "OK", IMG_ID

            return event_input_value, "ERROR: Image not found", IMG_ID

    def __del__(self):
        pass
