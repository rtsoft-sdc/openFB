import torch
import numpy as np


class PytorchHubModel:
    def __init__(self) -> None:
        self.status = "OK"

    def filter_bboxes_by_threshold(self, bbox_objects, threshold=0.5):
        filtered_bboxes = [obj for obj in bbox_objects if obj['confidence'] >= threshold]
    return filtered_bboxes

    def filter_bboxes_by_class(self, bbox_objects, cl_name='defect):
        filtered_bboxes = [obj for obj in bbox_objects if obj['class'] == cl_name]
    return filtered_bboxes
    
    def schedule(self, event_input_name, event_input_value, QI, PATH, THRESHOLD, IMAGE):
        'Write your code here.'
        if event_input_name == 'INIT':
            "Write your handler for current event here."
            self.model = torch.hub.load('WongKinYiu/yolov7', 'custom', PATH)

            return event_input_value, 0, QI, "OK", Data_IN

        if event_input_name == 'REQ':
            "Write your handler for current event here."
            if QI and str(Data_IN) in self.smd.keys():
                results = self.filter_bboxes_by_threshold(self.model(img), THRESHOLD)
		broken_obj = self.filter_bboxes_by_class(results)
		if len(broken) > 5 and len(broken) <= 10:
		    self.status = 'WARN'
		elif (len(broken) > 10:
		    self.status = "Error"
                return 0, event_input_value, QI, results, self.status
            else:
                return 0, event_input_value, QI, results, self.status
