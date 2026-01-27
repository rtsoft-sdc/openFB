import logging
from time import sleep
from shared_memory_dict import SharedMemoryDict
import numpy as np


class Merge4to1:
    def __init__(self) -> None:
        self.smd = ""
        image_shape = 1080  # max width, height parametr
        container_size = 15  # number of images that could be stored
        self.max_size = container_size*image_shape**2
    
    def __del__(self):
        # cleanup logic
        logging.debug("Object is being destroyed")
        try:
            if self.smd is SharedMemoryDict:
                del self.smd
        except Exception as err:
            logging.warning("Error occured during closing shared memory")
            logging.warning(err)

    def schedule(self, event_input_name, event_input_value, QI, QUEUE_ID, DATA_ID, X, Y, WIDTH, HEIGHT):
        'Write your code here.'
        if event_input_name == 'INIT':
            "Write your handler for current event here."
            sleep(1)
            self.smd = SharedMemoryDict(name=QUEUE_ID, size=self.max_size)
            return event_input_value, None, QI, None
        if event_input_name == 'REQ':
            "Write your handler for current event here."
            if QI and str(DATA_ID) in self.smd.keys():
                try:
                    data = np.array([X, Y, WIDTH, HEIGHT]).transpose(1, 0)
                    output = {"image": self.smd[str(
                        DATA_ID)]["image"], "detector": data}
                    self.smd[str(DATA_ID)] = output
                except:
                    logging.error("BROKEN DATA: %s" % [X, Y, WIDTH, HEIGHT])
                    logging.error(
                        f"Data shape is {data.shape}; Data:\n {data}")
                    return None, event_input_value, False, None

                return None, event_input_name, QI, DATA_ID
            else:
                return None, event_input_value, False, None
