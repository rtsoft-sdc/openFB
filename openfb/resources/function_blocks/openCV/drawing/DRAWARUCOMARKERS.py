import cv2
import numpy as np
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class DRAWARUCOMARKERS:

    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, CORNERS, IDS, DRAWCORNERS, DRAWAXIS):
        if event_input_name == 'REQ':
            queue_id = GlobalVideoMemory.get_queue_id(QUEUE_ID)
            img = GlobalVideoMemory.get(queue_id=queue_id, img_id=IMG_ID)
            if img is not None:
                try:
                    if DRAWCORNERS and len(CORNERS) > 1:
                        cv2.aruco.drawDetectedMarkers(img, CORNERS, IDS)
                        
                    if DRAWAXIS:
                        marker_length = 0.05 
                        
                        obj_points = np.array([
                            [-marker_length / 2,  marker_length / 2, 0],
                            [ marker_length / 2,  marker_length / 2, 0],
                            [ marker_length / 2, -marker_length / 2, 0],
                            [-marker_length / 2, -marker_length / 2, 0]
                        ], dtype=np.float32)
                            
                        camera_matrix = np.eye(3, dtype=np.float32)
                        dist_coeffs = np.zeros((5, 1), dtype=np.float32)
                            
                        for i in range(len(CORNERS)):
                            marker_corners = CORNERS[i].reshape(4, 2).astype(np.float32)
                        
                            success, rvec, tvec = cv2.solvePnP(
                                obj_points, 
                                marker_corners, 
                                camera_matrix, 
                                dist_coeffs, 
                                flags=cv2.SOLVEPNP_ITERATIVE
                            )
                                
                            if success:
                                cv2.drawFrameAxes(img, camera_matrix, dist_coeffs, rvec, tvec, 0.03)
                    return event_input_value, "OK", IMG_ID
                            
                except Exception as e:
                    print(f"Error in DRAWARUCOMARKERS: {e}")
                    return event_input_value, "ERROR drawarucomarkers", None

    def __del__(self):
        pass