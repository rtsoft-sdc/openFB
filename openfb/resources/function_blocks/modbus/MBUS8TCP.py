from openfb.resources.function_blocks.modbus.ModbusChannel import ModbusChannel
from openfb.resources.function_blocks.modbus.utils import parse_input_data_string, normalize_fb_id


class MBUS8TCP:
    def __init__(self):
        self.status = "CREATED"
        self.channel = None
        self.fb_registry = None
        
    def set_fb_registry(self, fb_registry):
        self.fb_registry = fb_registry

    def stop_channel(self):
        if self.channel:
            self.channel.stop()
            self.channel = None
            self.status = "STOPPED"
            
    def schedule(self, event_input_name, event_input_value, QI, PARAMS, IO0, IO1, IO2, IO3, IO4, IO5, IO6, IO7):
        if event_input_name == "MAP":
            if not QI:
                self.stop_channel()
                self.status = "DISABLED"
                return event_input_value, None, False, self.status
        
            try:
                self.address, self.port, self.unit_id = parse_input_data_string(PARAMS)
                if not self.address or not self.port:
                    self.status = "INVALID_PARAMS"
                    return event_input_value, None, False, self.status
                self.stop_channel()
                self.channel = ModbusChannel(address=self.address, port=self.port)
                
                if not self.channel.connect():
                    self.status = "CONNECTION_FAILED {} {}".format(self.address, self.port)
                    return event_input_value, None, False, self.status
                
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
                                                    
                    fb_wrapper.bind_channel(channel=self.channel)

                self.status = "CONNECTED {} {}".format(self.address, self.port)
                return event_input_value, event_input_value, True, self.status
            except Exception as e:
                self.status = f"ERROR: {str(e)}"
                return event_input_value, None, False, self.status
            
    def __del__(self):
        self.stop_channel()