import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class cvtColor():

    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, CODE, DSTCHANNEL):

        if event_input_name == 'REQ':
            img = GlobalVideoMemory.pop(QUEUE_ID, IMG_ID)
            if img is not None:
                code = f"COLOR_{CODE.upper()}"
                if hasattr(cv2, code):
                    CODE = getattr(cv2, code)
                else:
                    CODE = cv2.COLOR_BGR2GRAY
                img = cv2.cvtColor(img, CODE, dstCn=DSTCHANNEL)
                GlobalVideoMemory.push(QUEUE_ID, IMG_ID, img)
                return event_input_value, "OK", IMG_ID
            return event_input_value, "ERROR: Image not found", IMG_ID

    def __del__(self):
        pass
