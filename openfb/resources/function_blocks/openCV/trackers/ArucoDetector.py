import cv2
import logging
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class ArucoDetector():
    def __init__(self):
        self.detector = None
        self.current_dict_id = None
        
    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, DICTIONARY):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.pop(queue_id=QUEUE_ID, img_id=IMG_ID)
            if img is not None:
                try:
                    DICTIONARY = int(DICTIONARY)
                    if self.detector is None or self.current_dict_id != DICTIONARY:
                        self.detector = cv2.aruco.ArucoDetector(cv2.aruco.getPredefinedDictionary(DICTIONARY))
                        self.current_dict_id = DICTIONARY
                    corners, ids, rejected = self.detector.detectMarkers(img)
                    return event_input_value, IMG_ID, corners, ids, rejected, "OK"
                except Exception as e:
                    logging.error(f"Error initializing ArucoDetector: {e}")
                    return event_input_value, None, None, None, None, "ERROR: Invalid dictionary ID"
                        
    def __del__(self):
        logging.info("Delete ArucoDetector")
