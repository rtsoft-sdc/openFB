import time
import threading
import logging
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusServerContext, ModbusDeviceContext
from openfb.resources.function_blocks.io.flogic.base.ModbusSlaveChannel import ModbusSlaveChannel
from openfb.resources.function_blocks.io.flogic.base.ModbusSlaveChannelAdapter import ModbusSlaveChannelAdapter
from openfb.resources.function_blocks.io.flogic.base.utils import get_host_port_unitid
from openfb.resources.function_blocks.io.flogic.base.BaseProtocolFB import BaseProtocolFB

class BaseModbusServer(BaseProtocolFB):
    def __init__(self):
        super().__init__()
        self.host = None
        self.port = None
        self.unit_id = 1
        self.server_thread = None
        self.store = None
        self.MEMSIZE = 65536

    def _run_server(self, host, port, context: ModbusServerContext):
        try:
            StartTcpServer(context=context, address=(host, port))
        except Exception as e:
            logging.error(f"Error starting TCP server: {e}")

    def stop_channel(self):
        super().stop_channel()
        if self.server_thread and self.server_thread.is_alive():
            self.server_thread.join(timeout=2)
            self.server_thread = None

    def _start_server_and_bind(self, event_input_name, event_input_value, QI, PARAMS, io_blocks):
        if event_input_name != "MAP":
            return event_input_value, None, False, self.status

        if not QI:
            self.stop_channel()
            return event_input_value, None, False, "Disabled"

        try:
            self.host, self.port, unit_id, self.status = get_host_port_unitid(PARAMS)
            if not self.host or not self.port:
                return event_input_value, None, False, self.status
                
            self.unit_id = unit_id if unit_id is not None else 1

            self.stop_channel()
            
            device_context = ModbusDeviceContext(
                di=ModbusSequentialDataBlock(0x01, [0] * self.MEMSIZE),
                co=ModbusSequentialDataBlock(0x01, [0] * self.MEMSIZE),
                hr=ModbusSequentialDataBlock(0x01, [0] * self.MEMSIZE),
                ir=ModbusSequentialDataBlock(0x01, [0] * self.MEMSIZE),
            )

            self.store = ModbusServerContext(devices={self.unit_id: device_context}, single=False)
            self.channel = ModbusSlaveChannel(server_context=self.store)
            self.adapter = ModbusSlaveChannelAdapter(slave_channel=self.channel, default_unitid=self.unit_id)
            
            self.bind_and_connect_channels(io_blocks)

            self.server_thread = threading.Thread(
                target=self._run_server,
                args=(self.host, self.port, self.store),
                daemon=True
            )
            self.server_thread.start()
            time.sleep(0.1)

            self.status = f"LISTENING on {self.host}:{self.port}"
            return event_input_value, None, True, self.status
            
        except Exception as e:
            self.status = f"ERROR: {str(e)}"
            self.stop_channel()
            return event_input_value, None, False, self.status