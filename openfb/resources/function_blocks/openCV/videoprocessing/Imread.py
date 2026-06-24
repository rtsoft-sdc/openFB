import cv2
import logging

class Imread:
    def schedule(self, event_input_name, event_input_value, FILE_PATH, QUEUE_ID):
        if event_input_name == 'REQ':
            try:
                img = cv2.imread(FILE_PATH)
                if img is not None:
                    from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory
                    IMG_ID = GlobalVideoMemory.push(QUEUE_ID, img)
                    logging.debug(f"Image read successfully from {FILE_PATH} and pushed to queue {QUEUE_ID} with IMG_ID {IMG_ID}")
                    return event_input_value, IMG_ID, QUEUE_ID, "OK"
                else:
                    logging.error(f"Failed to read image from {FILE_PATH}. File may not exist or is not a valid image.")
                    return event_input_value, None, None, "ERROR"
            except Exception as e:
                logging.error(f"Error reading image from {FILE_PATH}: {e}")
                return event_input_value, None, None, "ERROR"