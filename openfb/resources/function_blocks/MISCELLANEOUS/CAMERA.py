import cv2
from shared_memory_dict import SharedMemoryDict


class CAMERA:
    def __init__(self) -> None:
        self.cap = ""
        self.smd = ""
        image_shape = 1080  # max width, height parametr
        container_size = 15  # number of images that could be stored
        self.max_size = container_size*image_shape**2
        self.QUEUE_ID = ""

    def schedule(self, event_input_name, event_input_value, QI, ID, PARAM, QUEUE_ID):
        'Write your code here.'
        if event_input_name == 'INIT':
            "Write your handler for current event here."
            self.smd = SharedMemoryDict(name=QUEUE_ID, size=self.max_size)
            # self.smd.clear()
            self.QUEUE_ID = QUEUE_ID
            # logging.error("Id % s" % QUEUE_ID)
            ID = int(ID) if ID.isdigit() else ID
            self.cap = cv2.VideoCapture(ID)
            return event_input_value, None, True, "Memory was prepared", None

        elif event_input_name == 'RSP':
            "Write your handler for current event here."
            if QI == True and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret == True:
                    if len(self.smd.keys()) == 0:
                        ind = 0
                    else:
                        ind = int(list(self.smd.keys())[-1])+1
                    ind = str(ind)
                    try:
                        self.smd[ind] = {"image": frame}
                        #cv2.imshow('img', frame)
                        #cv2.waitKey(1)
                    except ValueError:
                        self.smd[ind] = frame
                        self.smd.clear()
                    return None, event_input_value, True, "Image pushed", int(ind)
                else:
                    return None, event_input_name, False, "No image", None
            else:
                # logging.info(f"Stream state is {self.cap.isOpened()}")
                return None, event_input_name, False, "Stream maybe closed", None
