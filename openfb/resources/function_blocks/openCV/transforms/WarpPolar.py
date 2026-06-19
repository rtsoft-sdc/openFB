import cv2
import logging

from openfb.resources.function_blocks.openCV import CVsettings
from settings import get_interpolation_flag
from shared_memory_dict import SharedMemoryDict


class WarpPolar:
    def __init__(self):
        self.smd_connections = {}
        self.buffer_size = CVsettings.IMAGE_BUFFER_SIZE * CVsettings.IMAGE_HEIGHT * CVsettings.IMAGE_WIDTH * CVsettings.IMAGE_CHANNELS

    def schedule(
        self,
        event_input_name,
        event_input_value,
        IMG_ID,
        QUEUE_ID,
        DSIZE,
        CENTER,
        MAXRADIUS,
        FLAGS,
    ):
        if event_input_name == "REQ":
            if QUEUE_ID not in self.smd_connections:
                self.smd_connections[QUEUE_ID] = SharedMemoryDict(
                    name=QUEUE_ID, size=self.buffer_size
                )
            smd = self.smd_connections[QUEUE_ID]
            img_key = str(IMG_ID)
            data = smd.get(img_key)

            if data is not None:
                img = data["image"]
                dsize_tuple = (int(DSIZE[0]), int(DSIZE[1]))
                center_tuple = (int(CENTER[0]), int(CENTER[1]))
                maxradius_int = int(MAXRADIUS)
                flags_int = get_interpolation_flag(FLAGS)
                warped_img = cv2.warpPolar(
                    img, dsize_tuple, center_tuple, maxradius_int, flags_int
                )
                data["image"] = warped_img
                smd[img_key] = data
                return event_input_value, IMG_ID            

    def __del__(self):
        logging.info("Delete WarpPolar")
        for smd in self.smd_connections.values():
            del smd
