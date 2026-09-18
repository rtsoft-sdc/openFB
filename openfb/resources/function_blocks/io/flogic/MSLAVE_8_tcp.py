from openfb.resources.function_blocks.io.flogic.base.BaseModbusServer import BaseModbusServer

class MBUSLAVE8TCP(BaseModbusServer):
    def schedule(self, event_input_name, event_input_value, QI, PARAMS, 
                 IO0, IO1, IO2, IO3, IO4, IO5, IO6, IO7):
        return self._execute(
            event_input_name, event_input_value, QI, PARAMS, 
            [IO0, IO1, IO2, IO3, IO4, IO5, IO6, IO7]
        )