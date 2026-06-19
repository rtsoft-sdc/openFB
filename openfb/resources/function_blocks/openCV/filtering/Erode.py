import cv2
import logging
from shared_memory_dict import SharedMemoryDict
from openfb.resources.function_blocks.openCV import CVsettings

class Erode():
    def __init__(self):
        self.smd_connections = {}
        self.buffer_size = CVsettings.IMAGE_BUFFER_SIZE * CVsettings.IMAGE_HEIGHT * CVsettings.IMAGE_WIDTH * CVsettings.IMAGE_CHANNELS

    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, KERNEL, ANCHOR, ITERATIONS, BORDER_TYPE, BORDERVALUE):
        if event_input_name == 'REQ':
            if QUEUE_ID not in self.smd_connections:
                self.smd_connections[QUEUE_ID] = SharedMemoryDict(name=QUEUE_ID, size=self.buffer_size)
            smd = self.smd_connections[QUEUE_ID]
            img_key = str(IMG_ID)
            data = smd.get(img_key)
            if data is not None:
                img = data['image']
                cv2.erode(img, KERNEL, (ANCHOR[0], ANCHOR[1]), dst=img, iterations=ITERATIONS, borderType=BORDER_TYPE, borderValue=BORDERVALUE)
                smd[img_key] = data
                return event_input_value, IMG_ID
                
    def __del__(self):
        logging.info("Delete Erode")
        for smd in self.smd_connections.values():
            del smd