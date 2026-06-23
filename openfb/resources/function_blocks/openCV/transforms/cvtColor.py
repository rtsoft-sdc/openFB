import cv2
import logging
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class cvtColor():

    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, CODE, DSTCHANNEL):

        if event_input_name == 'REQ':
            img = GlobalVideoMemory.pop(QUEUE_ID, IMG_ID)
            if img is not None:
                code = f"COLOR_{CODE.upper()}"
                if hasattr(cv2, code):
                    CODE = getattr(cv2, code)
                else:
                    logging.error(f"Invalid color conversion code: {CODE}")
                    CODE = cv2.COLOR_BGR2GRAY
                img = cv2.cvtColor(img, CODE, dstCn=DSTCHANNEL)
                GlobalVideoMemory.push(QUEUE_ID, IMG_ID, img)
                return event_input_value, IMG_ID, QUEUE_ID, "OK"
            logging.error(f"No image found in GlobalVideoMemory for QUEUE_ID: {QUEUE_ID}, IMG_ID: {IMG_ID}")
            return event_input_value, IMG_ID, QUEUE_ID, "ERROR"

    def __del__(self):
        for smd in self.smd_connections.values():
            del smd
