from shared_memory_dict import SharedMemoryDict
from time import sleep


class IMG_QUEUE_DELETE:
    def __init__(self) -> None:
        self.smd = ""
        image_shape = 1080  # max width, height parametr
        container_size = 15  # number of images that could be stored
        self.max_size = container_size*image_shape**2
        self.QUEUE_ID = ""

    def __del__(self):
        if type(self.smd) == SharedMemoryDict:
            self.smd.shm.unlink()
            self.smd.shm.close()
            del self.smd

    def schedule(self, event_input_name, event_input_value, QI, IMG_ID, QUEUE_ID):
        'Write your code here.'
        if event_input_name == 'INIT':
            "Write your handler for current event here."
            sleep(1)
            self.smd = SharedMemoryDict(name=QUEUE_ID, size=self.max_size)
            return event_input_value, None, QI, "Init done."
        if event_input_name == 'RSP':
            "Write your handler for current event here."
            if str(IMG_ID) in self.smd.keys():
                id = str(IMG_ID)
                item = self.smd.pop(id)

                return None, event_input_value, QI, "Image with key % s was deleted." % id
            else:
                return None, event_input_value, QI, "The deletion was not performed: QI=False."
