from openfb.resources.function_blocks.io.flogic.ModbusSlaveChannel import ModbusSlaveChannel
from openfb.resources.function_blocks.io.flogic.ModbusSlaveChannelAdapter import ModbusSlaveChannelAdapter
from openfb.resources.function_blocks.io.flogic.utils import normalize_fb_id, get_host_port_unitid
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusServerContext, ModbusDeviceContext
import time
import threading
import logging

class MBUSLAVE8TCP:

    def __init__(self):
        self.channel = None
        self.adapter = None
        self.fb_registry = None
        self.server_thread = None
        self.store = None
        self.status = "Created"
        self.MEMSIZE = 65536
        self.fb_name = ""
        self.fb_prefix = "" 
        
    def set_fb_registry_and_name(self, fb_registry, fb_name):
        self.fb_registry = fb_registry
        self.fb_name = str(fb_name)
        self.fb_prefix = self.fb_name.rpartition('.')[0] + "."

        
    def _run_server(self, host, port, context: ModbusServerContext):
        try:
            StartTcpServer(context=context, address=(host, port))
        except Exception as e:
            logging.error(f"Error starting TCP server: {e}")

    def _stop_channel(self):
        if self.adapter:
            try:
                self.adapter.stop()
            except Exception as e:
                logging.error(f"Error stopping adapter: {e}")
            self.adapter = None
            
        if self.server_thread and self.server_thread.is_alive():
            self.server_thread.join(timeout=2)
            self.server_thread = None
        self.status = "Stopped"
        self.channel = None
        
    def _find_fb_object(self, ioblock_id):
            if not self.fb_registry:
                return None
            targetid = self.fb_prefix + normalize_fb_id(ioblock_id)
            if not targetid:
                return None
            for val in self.fb_registry.values():
                fb_name = getattr(val, "fb_name", '')
                if fb_name == targetid:
                    return getattr(val, 'fb_obj', None)
            return None
        
    def schedule(self, event_input_name, event_input_value, QI, PARAMS, 
                     IO0, IO1, IO2, IO3, IO4, IO5, IO6, IO7):
        if event_input_name == "MAP":
            if not QI:
                self._stop_channel()
                return event_input_value, None, False, "Disabled"
            try:
                self.host, self.port, unit_id, self.status = get_host_port_unitid(PARAMS)
                if not self.host or not self.port:
                    return event_input_value, None, False, self.status
                self.unit_id = unit_id if unit_id is not None else 1
                
                self._stop_channel()
                device_context = ModbusDeviceContext(
                    di = ModbusSequentialDataBlock(0x01, [0]*self.MEMSIZE), ##check 0x00
                    co = ModbusSequentialDataBlock(0x01, [0]*self.MEMSIZE),
                    hr = ModbusSequentialDataBlock(0x01, [0]*self.MEMSIZE),
                    ir = ModbusSequentialDataBlock(0x01, [0]*self.MEMSIZE),
                )

                self.store = ModbusServerContext(devices={self.unit_id:device_context}, single=False)
                self.channel = ModbusSlaveChannel(server_context=self.store)
                
                self.adapter = ModbusSlaveChannelAdapter(slave_channel=self.channel, default_unitid=self.unit_id)
                
                io_list = [IO0, IO1, IO2, IO3, IO4, IO5, IO6, IO7]
                for io_block in io_list:
                    fb_obj = self._find_fb_object(io_block)
                    if fb_obj and hasattr(fb_obj, 'bind_channel'):
                        try:
                            fb_obj.bind_channel(self.adapter)
                        except Exception as e:
                            logging.error(f"!!! {e}")

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
                return event_input_value, None, False, self.status
                

    def __del__(self):
        self._stop_channel()