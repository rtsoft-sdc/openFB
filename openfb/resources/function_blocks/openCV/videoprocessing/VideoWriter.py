# need to add ogl support 

import cv2
import numpy as np
import logging
from openfb.resources.function_blocks.openCV import CVsettings
from shared_memory_dict import SharedMemoryDict

class VideoWriter:
    def __init__(self):
        self.video_writer = None
        self.smd_connections = {}
        self.buffer_size = CVsettings.IMAGE_BUFFER_SIZE * CVsettings.IMAGE_HEIGHT * CVsettings.IMAGE_WIDTH * CVsettings.IMAGE_CHANNELS
        
    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, FILENAME, FOURCC, FPS, FRAME_SIZE, IS_COLOR, APIREFERENCE=None):
        if event_input_name == 'INIT':
            if APIREFERENCE is not None:
                self.video_writer = cv2.VideoWriter(FILENAME, APIREFERENCE, FOURCC, FPS, (FRAME_SIZE[0], FRAME_SIZE[1]), IS_COLOR)
            else:
                self.video_writer = cv2.VideoWriter(FILENAME, FOURCC, FPS, (FRAME_SIZE[0], FRAME_SIZE[1]), IS_COLOR)
                return event_input_value, None, FILENAME
        if event_input_name == 'REQ':
            if QUEUE_ID not in self.smd_connections:
                self.smd_connections[QUEUE_ID] = SharedMemoryDict(name=QUEUE_ID, size=self.buffer_size)
            smd = self.smd_connections[QUEUE_ID]
            img_key = str(IMG_ID)
            data = smd.get(img_key)
            if data is not None:
                img = data['image']
                self.video_writer.write(img)
                return event_input_value, IMG_ID, FILENAME
                                                                  
            return None, event_input_value, None


    def __del__(self):
        logging.info('Stopping VideoWriter')
        for smd in self.smd_connections.values():
            del smd
                    