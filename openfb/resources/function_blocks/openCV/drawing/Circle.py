import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class Circle():
    
    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, CENTER, RADIUS, COLOR, THICKNESS):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.pop(queue_id=QUEUE_ID, img_id=IMG_ID)

            if img is not None:
                cv2.circle(img, (int(CENTER[0]), int(CENTER[1])), int(RADIUS), (int(COLOR[0]), int(COLOR[1]), int(COLOR[2])), int(THICKNESS), dst=img)
                return event_input_value, "OK", IMG_ID

            return event_input_value, "ERROR: Image not found", None, 
    def __del__(self):
        pass