import numpy as np
import os
import cv2

class DETECTOR:

    def __init__(self):
        self.path = ""
        self.data = ""
        self.status = ""

    def schedule(self, event_input_name, event_input_value, path, name):

        if event_input_name == 'INIT':
            return [event_input_value, None, []]

        elif event_input_name == 'RUN':

            if path is None or name is None:
                status = "Error in specifying path/name"
                return [None, event_input_value, status]



            src_path = os.path.join(path, "{0}.png".format(name))
            dst_path = os.path.join(path, "inv_{0}.png".format(name))
            src = cv2.imread(src_path)
            dst = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
            output = np.array(dst)
            return [None, event_input_value, output]