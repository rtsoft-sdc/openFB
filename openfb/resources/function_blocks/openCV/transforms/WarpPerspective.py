import cv2
import logging
from openfb.resources.function_blocks.openCV import CVsettings
from shared_memory_dict import SharedMemoryDict
import numpy as np

class WarpPerspective:
    def __init__(self):
        self.smd_connections = {}
        self.buffer_size = CVsettings.IMAGE_BUFFER_SIZE * CVsettings.IMAGE_HEIGHT * CVsettings.IMAGE_WIDTH * CVsettings.IMAGE_CHANNELS
        
    def schedule(
        self,
        event_input_name,
        event_input_value,
        IMG_ID,
        QUEUE_ID,
        TRANSFORMATION_MATRIX,
        DSIZE,
        FLAGS,
        BORDERMODE,
        BORDERVALUE,
    ):
        if event_input_name == "REQ":
            if QUEUE_ID not in self.smd_connections:
                self.smd_connections[QUEUE_ID] = SharedMemoryDict(name=QUEUE_ID, size=self.buffer_size)
            smd = self.smd_connections[QUEUE_ID]
            img_key = str(IMG_ID)
            data = smd.get(img_key)
            if data is not None:
                img = data['image']
                if not isinstance(TRANSFORMATION_MATRIX, np.ndarray):
                    mat = np.array(TRANSFORMATION_MATRIX, dtype=np.float32)
                else:
                    mat = TRANSFORMATION_MATRIX.astype(np.float32)
                    mat = mat.reshape(3, 3)                
                    dsize = cv2.Size(DSIZE[0], DSIZE[1])
                    flag = f"INTER_{FLAGS.upper()}"
                    
                    img = cv2.warpPerspective(
                    img,
                    M=mat,
                    dsize=dsize,
                    flags=flag,
                    borderMode=BORDERMODE,
                    borderValue=BORDERVALUE,
                )
                data['image'] = img
                smd[img_key] = data
                return event_input_value, IMG_ID

    def __del__(self):
        logging.info("Delete WarpPerspective")
        for smd in self.smd_connections.values():
            del smd
