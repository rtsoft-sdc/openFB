import cv2
from openfb.resources.function_blocks.openCV import CVsettings
from shared_memory_dict import SharedMemoryDict
import logging
from settings import get_interpolation_flag

class WarpAffine:
    def __init__(self):
        self.smd_connections = {}
        self.fuffer_size = CVsettings.IMAGE_BUFFER_SIZE * CVsettings.IMAGE_HEIGHT * CVsettings.IMAGE_WIDTH * CVsettings.IMAGE_CHANNELS

    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, TRANSFORMATION_MATRIX, DSIZE, FLAGS, BORDERMODE, BORDERVALUE):
        if event_input_name == 'REQ':
            if QUEUE_ID not in self.smd_connections:
                self.smd_connections[QUEUE_ID] = SharedMemoryDict(name=QUEUE_ID, size=self.max_size)
            smd = self.smd_connections[QUEUE_ID]
            img_key = str(IMG_ID)
            data = smd.get(img_key)
            if data is not None:
                img = data['image']
                flags = get_interpolation_flag(FLAGS)
                Mat = TRANSFORMATION_MATRIX.reshape(2, 3)
                dsize = cv2.Size(DSIZE[0], DSIZE[1])
                img = cv2.warpAffine(img, M=Mat, dsize=dsize, flags=flags, borderMode=BORDERMODE, borderValue=BORDERVALUE)
                data['image'] = img
                smd[img_key] = data
                return event_input_value, IMG_ID
            
    def __del__(self):
        logging.info("Delete WarpAffine")
        for smd in self.smd_connections.values():
            del smd