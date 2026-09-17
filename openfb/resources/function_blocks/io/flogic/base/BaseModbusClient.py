from openfb.resources.function_blocks.io.flogic.base.ModbusChannel import ModbusChannel
from openfb.resources.function_blocks.io.flogic.base.ModbusChannelAdapter import ModbusChannelAdapter
from openfb.resources.function_blocks.io.flogic.base.utils import get_host_port_unitid
from openfb.resources.function_blocks.io.flogic.base.BaseProtocolFB import BaseProtocolFB

class BaseModbusClient(BaseProtocolFB):
    def __init__(self):
        super().__init__()
        self.address = None
        self.port = None
        self.unitid = 1

    def _connect_and_bind(self, event_input_name, event_input_value, QI, PARAMS, io_blocks):
        if event_input_name != "MAP":
            return event_input_value, None, False, self.status

        if not QI:
            self.stop_channel()
            self.status = "DISABLED"
            return event_input_value, None, False, self.status

        try:
            self.address, self.port, self.unitid, self.status = get_host_port_unitid(PARAMS)
            if not self.address or not self.port:
                self.status = f"Invalid params: {PARAMS}"
                return event_input_value, None, False, self.status

            self.stop_channel()
            self.channel = ModbusChannel(address=self.address, port=self.port)

            if not self.channel.connect():
                self.status = f"CONNECTION_FAILED {self.address} {self.port}"
                return event_input_value, None, False, self.status

            self.adapter = ModbusChannelAdapter(self.channel, self.unitid)
            
            self._connect_and_bind(io_blocks)

            self.status = f"CONNECTED {self.address} {self.port}"
            return event_input_value, event_input_value, True, self.status
            
        except Exception as e:
            self.status = f"Exception: {str(e)}"
            self.stop_channel()
            return event_input_value, None, False, self.status