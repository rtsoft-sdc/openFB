import logging
from openfb.resources.function_blocks.modbus.utils import parse_register_value

logger = logging.getLogger(__name__)

class ModbusIO:
    
    def __init__(self):
        self.channel = None
        self.unit_id = 1
        self.register_value = None
        self.register_type = None
        self.QO = False
        self.status = "Created"
        self.updated = False

    def bind_channel(self, channel):
        self.channel = channel
        
    def update_register(self, params):
        new_register_type, new_register_value = parse_register_value(params)
        if new_register_type is None or new_register_value is None:
            self.QO = False
            self.status = f"Invalid PARAMS: {params}"
            return False
        is_initial = self.register_value is None
        if (self.register_type, self.register_value) != (new_register_type, new_register_value):
            if not is_initial:
                self.updated = True
            self.register_type, self.register_value = new_register_type, new_register_value
        self.QO = True
        self.status = "OK"
        return True  
        
    def _init_block(self, QI, PARAMS):
        if not QI or not PARAMS:
            self.QO = False
            self.status = "Disabled"
            return False

        if self.channel is None:
            self.QO = False
            self.status = "Channel not bound"
            return False

        return self.update_register(PARAMS)

    def _check_ready(self, QI):
        if not QI:
            self.status = "Disabled"
            return False
        if self.channel is None or self.address is None:
            self.status = "Not initialized"
            return False
        return True