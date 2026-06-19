# need to add ogl support 

import cv2
import numpy as np
import logging
from shared_memory_dict import SharedMemoryDict

class VideoWriter:
    def __init__(self):
        self.video_writer = None
        self.smd = ""
        self.QUEUE_ID = ""

    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, FILENAME, FOURCC, FPS, FRAME_SIZE, IS_COLOR, APIREFERENCE=None):
        if event_input_name == 'INIT':
            if APIREFERENCE is not None:
                self.video_writer = cv2.VideoWriter(FILENAME, APIREFERENCE, FOURCC, FPS, (FRAME_SIZE[0], FRAME_SIZE[1]), IS_COLOR)
            else:
                self.video_writer = cv2.VideoWriter(FILENAME, FOURCC, FPS, (FRAME_SIZE[0], FRAME_SIZE[1]), IS_COLOR)
                return event_input_value, None, FILENAME
        if event_input_name == 'REQ':
            self.smd = SharedMemoryDict(name=QUEUE_ID, size=15*1080**2)
            if str(IMG_ID) in self.smd.keys():
                img = self.smd[str(IMG_ID)]
                self.video_writer.write(img)
                return None, event_input_value, None


    def __del__(self):
        logging.info('Stopping VideoWriter')
        if self.video_writer is not None:
            self.video_writer.release()
        self.smd.shm.close()
        self.smd.shm.unlink()
        del self.smd
        