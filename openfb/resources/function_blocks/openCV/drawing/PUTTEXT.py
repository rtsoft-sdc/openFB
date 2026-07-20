import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory
class PUTTEXT():
        
    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, ORG, TEXT, FONT_FACE, FONT_SCALE, COLOR, THICKNESS, BOTTOMLEFTORIGIN):
        if event_input_name == 'REQ':
            queue_id = GlobalVideoMemory.get_queue_id(QUEUE_ID)
            img = GlobalVideoMemory.get(queue_id=queue_id, img_id=IMG_ID)

            if img is not None:
                    cv2.putText(img, TEXT, (int(ORG[0]), int(ORG[1])), FONT_FACE, FONT_SCALE, (int(COLOR[0]), int(COLOR[1]), int(COLOR[2])), THICKNESS, BOTTOMLEFTORIGIN)
                    return event_input_value, "OK", IMG_ID
            return event_input_value, "ERROR: Image not found", None

    def __del__(self):
        pass