import cv2
import logging
from openfb.resources.function_blocks.openCV import CVsettings
from shared_memory_dict import SharedMemoryDict

class PutText():
    def __init__(self):
        self.smd_connections = {}
        self.buffer_size = CVsettings.IMAGE_BUFFER_SIZE * CVsettings.IMAGE_HEIGHT * CVsettings.IMAGE_WIDTH * CVsettings.IMAGE_CHANNELS
        
    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, ORG, TEXT, FONT_FACE, FONT_SCALE, COLOR, THICKNESS, BOTTOMLEFTORIGIN):
        if event_input_name == 'REQ':
            if QUEUE_ID not in self.smd_connections:
                self.smd_connections[QUEUE_ID] = SharedMemoryDict(name=QUEUE_ID, size=self.buffer_size)
            smd = self.smd_connections[QUEUE_ID]
            img_key = str(IMG_ID)
            data = smd.get(img_key)
            if data is not None:
                img = data['image']
                color_tuple = (int(COLOR[0]), int(COLOR[1]), int(COLOR[2]))
                org_tuple = (int(ORG[0]), int(ORG[1]))
                img = cv2.putText(img, TEXT, org_tuple, FONT_FACE, FONT_SCALE, color_tuple, THICKNESS, BOTTOMLEFTORIGIN)
                data['image'] = img
                smd[img_key] = data
                return event_input_value, IMG_ID

    def __del__(self):
        logging.info("Delete PutText")
        for smd in self.smd_connections.values():
            del smd