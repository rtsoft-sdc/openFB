from shared_memory_dict import SharedMemoryDict


class IMG_CONTAINER:
    def __init__(self) -> None:
        image_shape = 1080  # max width, height parametr
        container_size = 15  # number of images that could be stored
        self.max_size = container_size*image_shape**2
        self.shm = ""

    def schedule(self, event_input_name, event_input_value, QUEUE_ID, QI):
        'Write your code here.'
        if event_input_name == 'INIT':
            "Write your handler for current event here."
            self.shm = SharedMemoryDict(name=QUEUE_ID, size=self.max_size)
            return event_input_value, None, True, len(self.shm.keys())

        if event_input_name == 'RSP':
            "Write your handler for current event here."
            return event_input_value, event_input_value, True, len(self.shm.keys())
