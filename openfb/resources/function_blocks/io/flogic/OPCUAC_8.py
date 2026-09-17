from openfb.resources.function_blocks.io.flogic.base.BaseOpcUAClient import BaseOpcUAClient
class OPCUAC_8(BaseOpcUAClient):
    def schedule(self, event_input_name, event_input_value, QI, PARAMS, 
                 IO0, IO1, IO2, IO3, IO4, IO5, IO6, IO7):
        return self.bind_and_connect_channels(
            event_input_name, event_input_value, QI, PARAMS, 
            [IO0, IO1, IO2, IO3, IO4, IO5, IO6, IO7]
        )