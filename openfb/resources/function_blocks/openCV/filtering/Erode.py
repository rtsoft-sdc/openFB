import cv2
import logging
from openfb.resources.function_blocks.openCV import CVsettings
from openfb.resources.function_blocks.openCV.videoMemoryDict import VideoSharedMemory

class Erode():
    def __init__(self):
        self.buffer_size = CVsettings.IMAGE_BUFFER_SIZE * CVsettings.IMAGE_HEIGHT * CVsettings.IMAGE_WIDTH * CVsettings.IMAGE_CHANNELS
        self.smd = None
        self.queue_id = None

    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, KERNEL, ANCHOR, ITERATIONS, BORDER_TYPE, BORDERVALUE):
        if event_input_name == 'REQ':
            if QUEUE_ID != self.queue_id:
                self.smd = VideoSharedMemory(name=QUEUE_ID, size=self.buffer_size)
                self.queue_id = QUEUE_ID
            img = self.smd.get_frame(IMG_ID)

            if img is not None:
                cv2.erode(img, KERNEL, (ANCHOR[0], ANCHOR[1]), dst=img, iterations=ITERATIONS, borderType=BORDER_TYPE, borderValue=BORDERVALUE)
                return event_input_value, IMG_ID, QUEUE_ID, 'OK'
            logging.error(f"Failed to retrieve image with ID {IMG_ID} from shared memory queue {QUEUE_ID}")
            return event_input_value, None, None, 'ERROR'

    def __del__(self):
        logging.info("Delete Erode")