import os
import sys
import logging
from time import sleep
import numpy as np
from shared_memory_dict import SharedMemoryDict

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Tracking.detection import Detection
from Tracking.tracker import Tracker


class SORT:
    def __init__(self) -> None:
        self.smd = ""
        image_shape = 1080  # max width, height parametr
        container_size = 15  # number of images that could be stored
        self.max_size = container_size*image_shape**2
        self.track_ids = []

    def schedule(self, event_input_name, event_input_value, QI, N_INIT, MAX_AGE, IOU, QUEUE_ID, DATA_ID):
        'Write your code here.'
        if event_input_name == 'INIT':
            "Write your handler for current event here."
            sleep(1)
            self.smd = SharedMemoryDict(name=QUEUE_ID, size=self.max_size)
            self.tracker = Tracker(max_iou_distance=IOU,
                                   max_age=MAX_AGE, n_init=N_INIT)

            return event_input_value, None, QI, None

        if event_input_name == 'REQ':
            "Write your handler for current event here."
            if QI and str(DATA_ID) in self.smd:
                track_info = []
                try:
                    boxes = self.smd[str(DATA_ID)]["detector"]
                    detections = [Detection([x[0], x[1], x[2], x[3]])
                              for x in boxes]

                    tracks = self.tracker.update(detections)
                    for t in tracks:
                        track_box = t.to_tlwh()
                        if t.track_id not in self.track_ids:
                            self.track_ids.append(t.track_id)                    
                        logging.error(f"Track boxes. ID: {self.track_ids.index(t.track_id)}, X:{track_box[0]}, Y:{track_box[1]} W:{track_box[2]} H:{track_box[3]}")                        
                        track_info.append([self.track_ids.index(t.track_id), int(track_box[0]), int(
                            track_box[1]), int(track_box[2]), int(track_box[3])])
                        
                    input_data = self.smd[str(DATA_ID)]
                    output = {
                        "image": input_data["image"], "detector": input_data["detector"], "tracker": np.array(track_info)}
                    self.smd[str(DATA_ID)] = output
                    return None, event_input_name, QI, DATA_ID
                except Exception as e:
                    logging.error("Get exception: %s" % e)
                    # logging.error(track_info)
                    # logging.error("Detections: %s" % detections)

                    return None, event_input_name, False, None
            elif not QI:
                return None, event_input_name, False, DATA_ID
            else:
                return None, event_input_name, False, None

