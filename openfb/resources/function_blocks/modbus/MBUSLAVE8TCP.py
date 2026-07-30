from openfb.resources.function_blocks.modbus.ModbusSlaveChannel import ModbusSlaveChannel
from openfb.resources.function_blocks.modbus.utils import parse_input_data_string, normalize_fb_id
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
import time
import threading

class MBUSLAVE8TCP:

    def __init__(self):
        self.channel = None
        self.fb_registry = None
        self.server_thread = None
        self.store = None
        self.status = "Created"
        self.MEMSIZE = 65536 
        
    def set_fb_registry(self, fb_registry):
        self.fb_registry = fb_registry
        
    def _run_server(self, host, port, context: ModbusServerContext):
        StartTcpServer(context=context, address=(host, port))
        
    def _stop_channel(self):
        if self.server_thread and self.server_thread.is_alive():
            self.server_thread.join(timeout=2)
            self.server_thread = None
        self.status = "Stopped"
        self.channel = None
        
    def schedule(self, event_input_name, event_input_value, QI, PARAMS, 
                     IO0, IO1, IO2, IO3, IO4, IO5, IO6, IO7):
        if event_input_name == "MAP":
            if not QI:
                self._stop_channel()
                return None, None, False, "Disabled"
            try:
                self.host, self.port, self.unit_id = parse_input_data_string(PARAMS)
                self._stop_channel()
                slave_context = ModbusSlaveContext(
                    di=ModbusSequentialDataBlock(0, [0]*self.MEMSIZE), # Discrete Inputs
                    co=ModbusSequentialDataBlock(0, [0]*self.MEMSIZE), # Coils
                    hr=ModbusSequentialDataBlock(0, [0]*self.MEMSIZE), # Holding Registers
                    ir=ModbusSequentialDataBlock(0, [0]*self.MEMSIZE)  # Input Registers
                )
                
                self.store = ModbusServerContext(slaves={self.unit_id: slave_context}, single=False)
                self.channel = ModbusSlaveChannel(server_context=self.store)
                
                io_list = [IO0, IO1, IO2, IO3, IO4, IO5, IO6, IO7]
                for idx, io_block in enumerate(io_list):
                    io_block = normalize_fb_id(io_block)
                    if not io_block:
                        continue
                    fb_wrapper = None
                    for val in self.fb_registry.values():
                        if val.fb_name.split('.')[-1] == io_block:
                            fb_wrapper = val.fb_obj
                            break
                                                    
                    if fb_wrapper:
                        fb_wrapper.bind_channel(channel=self.channel)
                        fb_wrapper.unit_id = self.unit_id

                self.server_thread = threading.Thread(
                    target=self._run_server, 
                    args=(self.address, self.port, self.store),
                    daemon=True
                )
                self.server_thread.start()

                time.sleep(0.1)

                self.status = f"LISTENING on {self.address}:{self.port}"
                return event_input_value, None, True, self.status
            except Exception as e:
                self.status = f"ERROR: {str(e)}"
                return None, None, False, self.status
                

    def __del__(self):
        self._stop_channel()