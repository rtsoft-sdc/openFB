import torch


class PytorchHubModel:
    def schedule(self, event_input_name, event_input_value, QI, Model_src, Model_name, Data_IN):
        'Write your code here.'
        if event_input_name == 'INIT':
            "Write your handler for current event here."
            self.model = torch.hub.load(Model_src, Model_name)
            self.model.eval()
            return event_input_value, None, QI, "Model loaded", 0
        if event_input_name == 'REQ':
            "Write your handler for current event here."
            if QI:
                RES = self.model(Data_IN)
                return None, event_input_value, QI, "Check resuts", RES
            else:
                return None, event_input_value, QI, "Processing is locked", [0]
