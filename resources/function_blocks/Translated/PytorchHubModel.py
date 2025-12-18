from time import sleep
from shared_memory_dict import SharedMemoryDict
import torch


def Tensor2Int(x):
    return x.detach().cpu().numpy().astype('int16')


class PytorchHubModel:
    def __init__(self) -> None:
        self.smd = ""
        image_shape = 1080  # max width, height parametr
        container_size = 15  # number of images that could be stored
        self.max_size = container_size*image_shape**2

    def schedule(self, event_input_name, event_input_value, QI, Model_src, Model_name, QUEUE_ID, Data_IN):
        'Write your code here.'
        if event_input_name == 'INIT':
            "Write your handler for current event here."
            self.model = torch.hub.load(Model_src, Model_name)
            self.model.eval()
            sleep(1)
            self.smd = SharedMemoryDict(name=QUEUE_ID, size=self.max_size)

            return event_input_value, 0, QI, "Init", Data_IN

        if event_input_name == 'REQ':
            "Write your handler for current event here."
            if QI and str(Data_IN) in self.smd.keys():
                img = self.smd[str(Data_IN)]["image"]
                results = self.model(img)
                if "yolov5" in Model_name:
                    results = results.pred
                    results = map(Tensor2Int, results)
                    results = results[:, :4]
                self.smd[str(Data_IN)] = self.model(img)
                return 0, event_input_value, QI, "Data processed", Data_IN
            else:
                return 0, event_input_value, QI, "Queue is disabled", 0
