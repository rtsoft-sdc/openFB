# need to add ogl support 

import cv2
import logging
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class VideoWriter:
    def __init__(self):
        self.video_writer = None
        
    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, FILENAME, FOURCC, FPS, FRAME_SIZE, IS_COLOR, APIREFERENCE=None):
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
                    logging.error(f"Failed to open video writer with filename: {FILENAME}")
                    return event_input_value, IMG_ID, QUEUE_ID, "ERROR"
                logging.info(f"Video writer initialized with filename: {FILENAME}")
                return event_input_value, IMG_ID, QUEUE_ID, "OK"
            except Exception as e:
                logging.error(f"Error initializing video writer: {e}")
                return event_input_value, IMG_ID, QUEUE_ID, "ERROR"
            
        elif event_input_name == 'REQ':
            if self.video_writer is None:
                logging.error("Video writer not initialized. Please call INIT first.")
                return event_input_value, IMG_ID, QUEUE_ID, "ERROR"
            
            img = GlobalVideoMemory.pop(QUEUE_ID, IMG_ID)
            if img is not None:
                try:
                    self.video_writer.write(img)
                    logging.info(f"Frame written to video: IMG_ID={IMG_ID}, QUEUE_ID={QUEUE_ID}")
                    return event_input_value, IMG_ID, QUEUE_ID, "OK"
                except Exception as e:
                    logging.error(f"Error writing frame to video: {e}")
                    return event_input_value, IMG_ID, QUEUE_ID, "ERROR"
            else:
                logging.error(f"Image with ID {IMG_ID} not found in queue {QUEUE_ID}.")
                return event_input_value, IMG_ID, QUEUE_ID, "Image not found"
    def __del__(self):
        logging.info('Stopping VideoWriter')
        if self.video_writer is not None:
            self.video_writer.release()