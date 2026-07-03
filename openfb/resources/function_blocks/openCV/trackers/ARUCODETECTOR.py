import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class ARUCODETECTOR():
    def __init__(self):
        self.detector = None
        self.aruco_dict = cv2.aruco.DICT_6X6_250
        
    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, DICTIONARY): 
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.get(queue_id=QUEUE_ID, img_id=IMG_ID)
            if img is not None:
                try:
                    if self.detector is None or self.aruco_dict != DICTIONARY:
                        if hasattr(cv2.aruco, DICTIONARY):
                            self.aruco_dict = getattr(cv2.aruco, DICTIONARY)
                        else:
                            self.aruco_dict = cv2.aruco.DICT_6X6_250
                        aruco_dict = cv2.aruco.getPredefinedDictionary(self.aruco_dict)
                        self.detector = cv2.aruco.ArucoDetector(aruco_dict)
                                
                    corners, ids, rejected = self.detector.detectMarkers(img)
                    if corners is None or ids is None or len(corners) == 0 or len(ids) == 0:
                        corners, ids, rejected = [-1]*1024, [-1]*1024, [-1]*1024
                    return event_input_value, "OK", IMG_ID, len(ids), corners, ids, rejected
                except Exception as e:
                    print(f"Error in ArucoDetector: {e}")
                    return event_input_value, "ERROR arucodetector", None, None, None, None, None
            return event_input_value, "ERROR: no image found", None, None, None, None, None

    def __del__(self):
        pass