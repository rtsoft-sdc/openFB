from openfb.resources.function_blocks.io.flogic.base.BaseOpcUAClient import BaseOpcUAClient
class OPCUAC_18(BaseOpcUAClient):
    def schedule(self, event_input_name, event_input_value, QI, PARAMS, 
                 IO0, IO1, IO2, IO3, IO4, IO5, IO6, IO7, IO8, IO9, IO10, IO11, IO12, IO13, IO14, IO15, IO16, IO17):

        return self.bind_and_connect_channels(
            event_input_name, event_input_value, QI, PARAMS, 
            [IO0, IO1, IO2, IO3, IO4, IO5, IO6, IO7, IO8, IO9, IO10, IO11, IO12, IO13, IO14, IO15, IO16, IO17]
        )