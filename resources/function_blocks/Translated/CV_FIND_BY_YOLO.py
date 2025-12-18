from time import sleep
import cv2
import logging
from shared_memory_dict import SharedMemoryDict


class CV_FIND_BY_YOLO:
    def __init__(self) -> None:
        self.net = ""
        self.smd = ""
        image_shape = 1080  # max width, height parametr
        container_size = 15  # number of images that could be stored
        self.max_size = container_size*image_shape**2
        self.QUEUE_ID = ""

    def schedule(self, event_input_name, event_input_value, QI, QUEUE_ID, IMG_ID, NN_FILE, WEIGHTS_FILE,  CONFIDENCE, OBJECT_CLASS):
        'Write your code here.'
        if event_input_name == 'INIT':
            sleep(1)
            self.smd = SharedMemoryDict(name=QUEUE_ID, size=self.max_size)
            self.net = cv2.dnn.readNet(WEIGHTS_FILE, NN_FILE)
            # self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.model = cv2.dnn_DetectionModel(self.net)
            self.model.setInputParams(
                size=(416, 416), scale=1/255, swapRB=True)
            "Write your handler for current event here."
            return event_input_value, None, True, 0, 0, 0, 0, 0
        if event_input_name == 'REQ':
            "Write your handler for current event here."
            if QI == True:
                classes, scores, boxes = self.model.detect(
                    self.smd[str(IMG_ID)]["image"], CONFIDENCE, CONFIDENCE)

                if type(boxes) == tuple:
                    return None, event_input_value, False, [0], [0], [0], [0], []
                else:
                    return None, event_input_value, QI, boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3], len(boxes)
            else:
                return None, event_input_value, QI, [0], [0], [0], [0], [0]
