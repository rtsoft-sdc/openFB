import cv2
import logging
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class Imwrite:

    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, FILE_PATH):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.pop(queue_id=QUEUE_ID, img_id=IMG_ID)
            if img is not None:
                try:
                    cv2.imwrite(FILE_PATH, img)
                    logging.debug(f"Image saved to {FILE_PATH}")
                    return event_input_value, IMG_ID, QUEUE_ID, FILE_PATH, "OK"
                except Exception as e:
                    logging.error(f"Failed to save image to {FILE_PATH}: {e}")
                    return event_input_value, None, None, None, "Failed to save image"
            else:
                logging.debug("No image found in the specified queue and ID.")
                return event_input_value, None, None, None, "No image found"
        else:
            logging.debug(f"Unsupported event input name: {event_input_name}")
            return event_input_value, None, None, None, "Unsupported event input name"