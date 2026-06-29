import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class RECTANGLE():
        
    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, PT1, PT2, COLOR, THICKNESS):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.get(queue_id=QUEUE_ID, img_id=IMG_ID)
            
            if img is not None:
                cv2.rectangle(img, (int(PT1[0]), int(PT1[1])), (int(PT2[0]), int(PT2[1])), (int(COLOR[0]), int(COLOR[1]), int(COLOR[2])), int(THICKNESS), dst=img)
                return event_input_value, "OK", IMG_ID
            return event_input_value, "ERROR: Image not found", None

    def __del__(self):
        pass