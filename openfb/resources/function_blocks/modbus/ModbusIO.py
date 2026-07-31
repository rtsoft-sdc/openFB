import logging
from openfb.resources.function_blocks.modbus.utils import parse_io_params

logger = logging.getLogger(__name__)

class ModbusIO:
    
    def __init__(self):
        self.channel = None
        self.unit_id = 1
        self.address = None
        self.register_type = None
        self.QO = False
        self.status = "Created"
        self.updated = False

    def bind_channel(self, channel):
        self.channel = channel

    def _init_block(self, QI, PARAMS):
        if not QI or not PARAMS:
            self.QO = False
            self.status = "Disabled"
            return False

        if self.channel is None:
            self.QO = False
            self.status = "Channel not bound"
            return False

        try:
            new_address, new_register_type = parse_io_params(PARAMS)
            if (self.address, self.register_type) != (new_address, new_register_type):
                 if self.address is not None:
                     self.updated = True
                 self.address, self.register_type = new_address, new_register_type
            self.QO = True
            self.status = "OK"
            return True
        except Exception as e:
            self.QO = False
            self.status = f"{str(e)}"
            logger.error(f"{self.status}")
            return False

    def _check_ready(self, QI):
        if not QI:
            self.status = "Disabled"
            return False
        if self.channel is None or self.address is None:
            self.status = "Not initialized"
            return False
        return True