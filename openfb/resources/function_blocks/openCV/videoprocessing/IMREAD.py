import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class IMREAD:
    def schedule(self, event_input_name, event_input_value, QUEUE_ID, FILE_PATH):
        if event_input_name == 'REQ':
            try:
                img = cv2.imread(FILE_PATH)
                if img is not None:
                    IMG_ID = GlobalVideoMemory.set(QUEUE_ID, img)
                    return event_input_value, IMG_ID, QUEUE_ID, "OK"
                else:
                    return event_input_value, "ERROR: could not read image", None
            except Exception as e:
                return event_input_value, "ERROR: " + str(e), None