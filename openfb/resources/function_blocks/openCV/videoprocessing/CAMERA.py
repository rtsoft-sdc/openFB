import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory 

class CAMERA:
    def __init__(self) -> None:
        self.cap = None
        self.QUEUE_ID = "default_queue"
        self.imgIDcounter = 0

    def __del__(self):
        try:
            if self.cap is not None and not isinstance(self.cap, str):
                self.cap.release()
        except Exception as e:
            print(f"Error releasing camera: {e}")

    def schedule(self, event_input_name, event_input_value, QI, ID, QUEUE_ID):
        if event_input_name == 'INIT':
            if self.cap is not None:
                self.cap.release()
            if QUEUE_ID:
                self.QUEUE_ID = QUEUE_ID
            else:
                self.QUEUE_ID = "default_queue"
            ID = int(ID) if ID.isdigit() else ID
            self.cap = cv2.VideoCapture(ID)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            if not self.cap.isOpened():
                return event_input_value, None, False, "Failed to open camera", None
            return event_input_value, None, True, "Camera initialized", None
            
        elif event_input_name == 'REQ':
            if QI and self.cap is not None and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret == True:
                    current_id = self.imgIDcounter
                    GlobalVideoMemory.set(queue_id=self.QUEUE_ID, img_id=current_id, frame=frame)
                    self.imgIDcounter += 1
                    return None, event_input_value, True, "Frame captured", current_id 
                
                else:
                    return None, event_input_value, False, "Failed to capture frame", None