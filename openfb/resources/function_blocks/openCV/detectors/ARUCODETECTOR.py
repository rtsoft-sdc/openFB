import cv2
import numpy as np
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class ARUCODETECTOR():
    def __init__(self):
        self.detector = None
        self.aruco_dict = cv2.aruco.DICT_6X6_250        
        
    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, DICTIONARY): 
        if event_input_name == 'REQ':
            queue_id = GlobalVideoMemory.get_queue_id(QUEUE_ID)
            img = GlobalVideoMemory.get(queue_id=queue_id, img_id=IMG_ID)
            if img is not None:
                try:
                    if self.detector is None or self.aruco_dict != DICTIONARY:
                        if hasattr(cv2.aruco, DICTIONARY):
                            self.aruco_dict = getattr(cv2.aruco, DICTIONARY)
                        else:
                            self.aruco_dict = cv2.aruco.DICT_6X6_250
                        aruco_dict = cv2.aruco.getPredefinedDictionary(self.aruco_dict)
                        self.detector = cv2.aruco.ArucoDetector(aruco_dict)
                                
                    corners, ids, _ = self.detector.detectMarkers(img)
                    if ids is not None and len(corners) > 0:
                        corners = np.array(corners).flatten().tolist()
                        ids = ids.flatten().tolist()
                        markercount = len(ids)
                    else:
                        markercount, corners, ids = 0, [0], [0]
                    return event_input_value, "OK", IMG_ID, markercount, corners, ids
                except Exception as e:
                    return event_input_value, f"ERROR arucodetector {e}", None, None, None, None
            return event_input_value, "ERROR: no image found", None, None, None, None

    def __del__(self):
        pass