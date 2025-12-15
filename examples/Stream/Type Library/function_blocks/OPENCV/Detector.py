import os
import cv2
import torch

class Detector:

    def __init__(self):
        """ Not necessary block of code. Can be used as a storage. """
        self.model=[]
        self.path = ""
        self.data = ""
        self.status = ""

    def schedule(self, event_input_name, event_input_value, model_name, path, im_name):
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
            # self.model  = torch.hub.load('ultralytics/yolov5', model_name)
            return [event_input_value, None, "LOADED", None]

        elif event_input_name == 'REQ':
            # img = os.path.join(path, im_name)
            # result = self.model(img)
            # output = result.print()
            return [None, event_input_value, "DONE", model_name]