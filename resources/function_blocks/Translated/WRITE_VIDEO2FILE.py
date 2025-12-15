import logging
from time import sleep
import cv2
from shared_memory_dict import SharedMemoryDict


class WRITE_VIDEO2FILE:
    def __init__(self) -> None:
        self.smd = ""
        image_shape = 1080  # max width, height parametr
        container_size = 15  # number of images that could be stored
        self.max_size = container_size*image_shape**2
        self.QUEUE_ID = ""

    def schedule(self, event_input_name, event_input_value, QI, QUEUE_ID, filepath, IMG_ID):
        'Write your code here.'
        if event_input_name == 'INIT':
            "Write your handler for current event here."
            sleep(1)
            self.smd = SharedMemoryDict(name=QUEUE_ID, size=self.max_size)
            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            self.video_writer = cv2.VideoWriter(
                filepath, fourcc, 30, (640, 480))
            return event_input_value, None, QI
        if event_input_name == 'REQ':
            "Write your handler for current event here."
            frame = self.smd[str(IMG_ID)]["image"]
            self.video_writer.write(frame)
            logging.error(f"Input value is {event_input_value}")
            return None, event_input_value, QI
