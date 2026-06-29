import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class ARUCODETECTOR():
    def __init__(self):
        self.detector = None
        self.current_dict_id = None
        
    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, DICTIONARY):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.get(queue_id=QUEUE_ID, img_id=IMG_ID)
            if img is not None:
                try:
                    DICTIONARY = cv2.aruco.DICT_6X6_250
                    if self.detector is None or self.current_dict_id != DICTIONARY:
                        self.detector = cv2.aruco.ArucoDetector(cv2.aruco.getPredefinedDictionary(DICTIONARY))
                        self.current_dict_id = DICTIONARY
                    corners, ids, rejected = self.detector.detectMarkers(img)
                    return event_input_value, "OK", IMG_ID, corners, ids, rejected
                except Exception as e:
                    print(f"Error in ArucoDetector: {e}")
                    return event_input_value, "ERROR arucodetector", None, None, None, None
            return event_input_value, "ERROR: no image found", None, None, None, None

    def __del__(self):
        pass