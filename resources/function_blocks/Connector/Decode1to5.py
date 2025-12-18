import logging
from time import sleep
from shared_memory_dict import SharedMemoryDict


class Decode1to5:
    def __init__(self) -> None:
        self.smd = ""
        image_shape = 1080  # max width, height parametr
        container_size = 15  # number of images that could be stored
        self.max_size = container_size*image_shape**2

    def schedule(self, event_input_name, event_input_value, QI, QUEUE_ID, DATA_ID):
        'Write your code here.'
        if event_input_name == 'INIT':
            "Write your handler for current event here."
            sleep(1)
            self.smd = SharedMemoryDict(name=QUEUE_ID, size=self.max_size)
            return event_input_value, None, QI, None, None, None, None, None, None
        if event_input_name == 'REQ':
            "Write your handler for current event here."
            if QI and str(DATA_ID) in self.smd.keys():
                # logging.error(self.smd[str(DATA_ID)])
                data = self.smd[str(DATA_ID)]["tracker"]
                return None, event_input_value, QI, DATA_ID, data[:, 0], data[:, 1], data[:, 2], data[:, 3], data[:, 4]
            else:
                return None, event_input_value, QI, None, None, None, None, None, None
