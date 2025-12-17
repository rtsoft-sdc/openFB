import os
import cv2
from time import sleep
from shared_memory_dict import SharedMemoryDict


class Draw_box:
    def __init__(self) -> None:
        self.smd = ""
        image_shape = 1080  # max width, height parametr
        container_size = 15  # number of images that could be stored
        self.max_size = container_size*image_shape**2
        self.QUEUE_ID = ""
        self.dir = os.path.abspath(__file__)
        self.thick = 2
        self.color = (255, 0, 0)

    def schedule(self, event_input_name, event_input_value, QI, X, Y, Width, Height, QUEUE_ID, IMG_ID):
        'Write your code here.'
        if event_input_name == 'INIT':
            "Write your handler for current event here."
            sleep(1)
            self.smd = SharedMemoryDict(name=QUEUE_ID, size=self.max_size)

            return event_input_value, None, QI, IMG_ID, "Module init"

        if event_input_name == 'RUN':
            "Write your handler for current event here."
            if str(IMG_ID) in self.smd.keys() and QI:
                img = self.smd[str(IMG_ID)]["image"]
                dst = img
                if type(X) != int:
                    for b in range(len(X)):
                        dst = cv2.rectangle(
                            img, (X[b], Y[b]), (X[b] + Width[b], Y[b] + Height[b]), self.color, self.thick)
                filename = f"{IMG_ID}.png"
                cv2.imwrite(os.path.join(self.dir, "resources", filename), dst)
                self.smd[str(IMG_ID)] = {"image": dst}
                return None, event_input_value, QI, IMG_ID, "Check check iamge in resources folder "
            else:
                return None, event_input_value, QI, IMG_ID, "Something wrong"
