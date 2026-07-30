from openfb.resources.function_blocks.modbus.utils import parse_params
import numpy as np

#get_modbus_node
class QL:    
    def __init__(self):
        self.QO = False
        self.STATUS = "CREATED"
    
        self.channel = None        
        self.address = None
        self.unit_id = 1
    
    def set_channel(self, channel):
        self.channel = channel
    
    def schedule(self, event_input_name, event_input_value, QI, PARAMS, IN):
        if event_input_name == "INIT":
            if not QI:
                self.QO = False
                self.STATUS = "DISABLED"
                return None, event_input_value, self.QO, self.STATUS
            if self.channel is None or not self.channel.connected: #is_connected
                self.QO = False
                self.STATUS = "NODE_NOT_CONNECTED"
                return None, event_input_value, self.QO, self.STATUS
            try: 
                self.address, self.unit_id = parse_params(PARAMS)
                self.QO = True
                self.STATUS = "INITIALIZED"
                return event_input_value, None, self.QO, self.STATUS
            except Exception as e:
                self.STATUS = f"ERROR: {str(e)}"
                self.QO = False
                return None, event_input_value, self.QO, self.STATUS
        if event_input_name == "REQ":
            if not QI:
                self.STATUS = "DISABLED"
                return None, event_input_value, self.QO, self.STATUS
            if not self.QO or self.channel is None or not self.address:
                self.STATUS = "NOT_INITIALIZED"
                return None, event_input_value, self.QO, self.STATUS
            try: 
                self.channel.write_coil(address=self.address, value=np.longdouble(IN), slave=self.unit_id) # long double
                self.STATUS = "OK"
                return None, event_input_value, self.QO, self.STATUS
            except Exception as e:
                self.STATUS = f"ERROR: {str(e)}"
                self.QO = False
                return None, event_input_value, self.QO, self.STATUS
    def __del__(self):
        self.node_client = None