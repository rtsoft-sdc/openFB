import os
import cv2

class READER2:

    def __init__(self):
        """ Not necessary block of code. Can be used as a storage. """
        self.path = ""
        self.data = ""
        self.status = ""

    def schedule(self, event_input_name, event_input_value, path, name):
        """ Main function that will be called by platform.
        Args:
            ****** Common arguments ****
            event_input_name (str): Name of input event that was called
            event_input_value (any): Any object that could be handled
            ******* End of common arguments
            
            ****  Different part ****
            Any number of inputs depends on your block design (can be names as you want)
        Returns:
            list of outputs for ouput events and ouputs
            [output_e1, output_e3.., output1, .. outputN]
        """

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
            cv2.imwrite(dst_path, dst)
            return [None, event_input_value, "OK"]