from openfb.resources.function_blocks.modbus.ModbusChannel import ModbusChannel
from openfb.resources.function_blocks.modbus.utils import normalize_fb_id, get_host_port_unitid
from openfb.resources.function_blocks.modbus.ModbusChannelAdapter import ModbusChannelAdapter
import logging 

class MBUS8TCP:
    def __init__(self):
        self.status = "CREATED"
        self.channel = None
        self.fb_registry = None
        self.adapter = None
        self.address = None
        self.port = None
        self.unitid = 1
        
    def set_fb_registry(self, fb_registry):
        self.fb_registry = fb_registry

    def stop_channel(self):
        if self.adapter:
            try:
                self.adapter.stop()
            except Exception as e:
                logging.error(f"Error {e}")
            self.adapter = None
            self.channel = None
        if self.channel:
            try:
                self.channel.stop()
            except Exception as e:
                logging.error(f"Eror {e}")
            self.channel = None
        self.status = "STOPPED"
        
    def _find_fb_object(self, ioblock_id):
        if not self.fb_registry:
            return None
        targetid = normalize_fb_id(ioblock_id)
        if not targetid:
            return None
        print(f"\n\nNOW:\n {self.fb_registry.values()}")##############
        for val in self.fb_registry.values():
            fb_name = getattr(val, "fb_name", '')
            if fb_name.split('.')[-1] == targetid:
                return getattr(val, 'fb_obj', None)
        return None
            

    def schedule(self, event_input_name, event_input_value, QI, PARAMS, IO0, IO1, IO2, IO3, IO4, IO5, IO6, IO7):
        if event_input_name == "MAP":
            if not QI:
                self.stop_channel()
                self.status = "DISABLED"
                return event_input_value, None, False, self.status
        
            try:
                self.address, self.port, unitid, self.status = get_host_port_unitid(PARAMS)
                if not self.address or not self.port:
                    self.status = f"Invalid params: {PARAMS}"
                    return event_input_value, None, False, self.status
                self.unitid = unitid if unitid is not None else 1
                
                self.stop_channel()
                self.channel = ModbusChannel(address=self.address, port=self.port)
                
                if not self.channel.connect():
                    self.status = "CONNECTION_FAILED {} {}".format(self.address, self.port)
                    return event_input_value, None, False, self.status
                
                adapter = ModbusChannelAdapter(self.channel, self.unitid)
                
                io_list = [IO0, IO1, IO2, IO3, IO4, IO5, IO6, IO7]
                for io_block in io_list:
                    if not io_block:
                        continue
                    
                    fb_obj = self._find_fb_object(io_block)
                    if fb_obj and hasattr(fb_obj, 'bind_channel'):
                        fb_obj.bind_channel(self.adapter)
                    else:
                        logging.warning(f"no 'bind_channel' attribute")
                    
                self.status = "CONNECTED {} {}".format(self.address, self.port)
                return event_input_value, event_input_value, True, self.status
            except Exception as e:
                self.status = f"Exception in MBUS8TCP: {str(e)}"
                self.stop_channel()
                
                return event_input_value, None, False, self.status
            
    def __del__(self):
        self.stop_channel()