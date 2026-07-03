import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class IMWRITE:

    def schedule(self, event_input_name, event_input_value, QI, IMG_ID, QUEUE_ID, FILE_PATH):
        if event_input_name == 'REQ' and QI:
            queue_id = GlobalVideoMemory.get_queue_id(QUEUE_ID)
            img = GlobalVideoMemory.get(queue_id=queue_id, img_id=IMG_ID)
            if img is not None:
                try:
                    cv2.imwrite(FILE_PATH, img)
                    return event_input_value, True, "OK", IMG_ID
                except Exception as e:
                    return event_input_value, False, f"Failed to save image to {FILE_PATH}: {e}", IMG_ID
            else:
                return event_input_value, False, "No image found", None