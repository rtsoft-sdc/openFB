import cv2
import numpy as np
import logging
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class DRAWARUCOMARKERS:

    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, MARKERCOUNT, CORNERS, IDS, DRAWCORNERS, DRAWAXIS):
        if event_input_name == 'REQ':
            queue_id = GlobalVideoMemory.get_queue_id(QUEUE_ID)
            img = GlobalVideoMemory.get(queue_id=queue_id, img_id=IMG_ID)
            if img is not None:
                try:
                    if DRAWCORNERS and MARKERCOUNT > 0:
                        markers_num = int(len(CORNERS)/8)
                        np_corners = np.array(CORNERS, dtype=np.float32).reshape(markers_num, 1, 4, 2)
                        formatted_corners = [np_corners[i] for i in range(markers_num)]
                        np_ids = np.array(IDS, dtype=np.float32).reshape(markers_num, 1)
                        cv2.aruco.drawDetectedMarkers(img, formatted_corners, np_ids)
                    if DRAWAXIS and MARKERCOUNT > 0:
                        marker_length = 0.05 
                        
                        obj_points = np.array([
                            [-marker_length / 2,  marker_length / 2, 0],
                            [ marker_length / 2,  marker_length / 2, 0],
                            [ marker_length / 2, -marker_length / 2, 0],
                            [-marker_length / 2, -marker_length / 2, 0]
                        ], dtype=np.float32)
                            
                        camera_matrix = np.eye(3, dtype=np.float32)
                        dist_coeffs = np.zeros((5, 1), dtype=np.float32)
                        
                        for i in range(MARKERCOUNT):
                            start_idx = i * 8
                            end_idx = start_idx + 8
                            marker_corners = np.array(CORNERS[start_idx:end_idx], dtype=np.float32).reshape(4, 2)
                        
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
                    logging.error(f"Error in DRAWARUCOMARKERS: {e}")
                    return event_input_value, f"ERROR drawarucomarkers {e}", None

    def __del__(self):
        pass