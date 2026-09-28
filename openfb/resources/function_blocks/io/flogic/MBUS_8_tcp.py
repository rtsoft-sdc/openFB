from openfb.resources.function_blocks.io.flogic.base.BaseModbusClient import BaseModbusClient

class MBUS_8_tcp(BaseModbusClient):
    def schedule(self, event_input_name, event_input_value, QI, PARAMS, 
                 IO0, IO1, IO2, IO3, IO4, IO5, IO6, IO7):
        return self._execute(
            event_input_name, event_input_value, QI, PARAMS, 
            [IO0, IO1, IO2, IO3, IO4, IO5, IO6, IO7]
        )