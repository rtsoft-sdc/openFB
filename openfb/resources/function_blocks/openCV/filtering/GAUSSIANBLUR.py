import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class GAUSSIANBLUR():

    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, KSIZE, SIGMAX, SIGMAY):
        if event_input_name == 'REQ':
            queue_id = GlobalVideoMemory.get_queue_id(QUEUE_ID)
            img = GlobalVideoMemory.get(queue_id=queue_id, img_id=IMG_ID)

            if img is not None:
                img = cv2.GaussianBlur(img, ksize=(KSIZE[0], KSIZE[1]), sigmaX=SIGMAX, sigmaY=SIGMAY, dst=img)
                return event_input_value, "OK", IMG_ID
            return event_input_value, "ERROR: no image found", None

    def __del__(self):
        pass