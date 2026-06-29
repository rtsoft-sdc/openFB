import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class VIDEOWRITER:
    def __init__(self):
        self.video_writer = None
        
    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, FILENAME, FOURCC, FPS, FRAME_SIZE, IS_COLOR, APIREFERENCE=None):
        if event_input_name == 'INIT':
            try:
                if self.video_writer is not None:
                    self.video_writer.release()
                frame_size_tuple = (int(FRAME_SIZE[0]), int(FRAME_SIZE[1]))
                
                if isinstance(FOURCC, str):
                    fourcc = cv2.VideoWriter_fourcc(*FOURCC)
                else:
                    fourcc = FOURCC

                if APIREFERENCE is not None:
                    self.video_writer = cv2.VideoWriter(FILENAME, fourcc, FPS, frame_size_tuple, IS_COLOR, apiPreference=APIREFERENCE)
                else:
                    self.video_writer = cv2.VideoWriter(FILENAME, fourcc, FPS, frame_size_tuple, IS_COLOR)
                    
                if not self.video_writer.isOpened():
                    return event_input_value, "ERROR: Failed to open video writer", IMG_ID
                return event_input_value, "OK", IMG_ID
            except Exception as e:
                return event_input_value, "ERROR: Failed to initialize video writer", IMG_ID
            
        elif event_input_name == 'REQ':
            if self.video_writer is None:
                return event_input_value, "ERROR: Video writer not initialized. Please call INIT first.", IMG_ID
            
            img = GlobalVideoMemory.get(QUEUE_ID, IMG_ID)
            if img is not None:
                try:
                    self.video_writer.write(img)
                    return event_input_value, "OK", IMG_ID
                except Exception as e:
                    return event_input_value, "ERROR: Failed to write frame to video", IMG_ID
            else:
                return event_input_value, "ERROR: Image not found", IMG_ID
    
    def __del__(self):
        if self.video_writer is not None:
            self.video_writer.release()