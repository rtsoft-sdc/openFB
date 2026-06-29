import cv2
import logging
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory 

class CAMERA:
    def __init__(self) -> None:
        self.cap = None
        self.QUEUE_ID = None
        self.imgIDcounter = 0

    def __del__(self):
        try:
            if self.cap is not None and not isinstance(self.cap, str):
                self.cap.release()
                logging.debug("Camera object is destroyed")
        except Exception as e:
            logging.error(f"Error occurred while releasing camera: {e}")

    def schedule(self, event_input_name, event_input_value, QI, ID, QUEUE_ID):
        if event_input_name == 'INIT':
            if self.cap is not None:
                self.cap.release()
            self.QUEUE_ID = QUEUE_ID
            ID = int(ID) if ID.isdigit() else ID
            self.cap = cv2.VideoCapture(ID)
            if not self.cap.isOpened():
                logging.error(f"Failed to open camera with ID: {ID}")
                return event_input_value, None, False, "Failed to open camera", None
            logging.info(f"Camera initialized with ID: {ID}")
            return event_input_value, None, True, "Camera initialized", None
            
        elif event_input_name == 'REQ':
            if QI  and self.cap is not None and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret == True:
                    current_id = self.imgIDcounter
                    GlobalVideoMemory.set(queue_id=self.QUEUE_ID, img_id=current_id, frame=frame)
                    self.imgIDcounter += 1
                    logging.info(f"Frame captured and stored with ID: {current_id}")
                    return None, event_input_value, True, "Frame captured", current_id 
                
                else:
                    logging.error("Failed to capture frame from camera")
                    return None, event_input_value, False, "Failed to capture frame", None