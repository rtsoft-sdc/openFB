from openfb.resources.function_blocks.io.AbstractChannel import AbstractChannel
from openfb.resources.function_blocks.modbus.ModbusChannel import ModbusChannel

class ModbusChannelAdapter(AbstractChannel):
    
    def __init__(self, modbus_channel: ModbusChannel, default_unitid: int = 1):
        self.channel = modbus_channel
        self.default_unitid = default_unitid
        
    def read_data(self, address, datatype):
        reg_type, reg_value = address
        if datatype in ("QX", "IX", "BOOL"):
            return self.channel.read_bit_sequence(
                address=reg_value, bit_count=1, reg_type=reg_type, device_id=self.default_unit_id
            )
        else:
            return self.channel.read_register_sequence(
                address=reg_value, reg_count=1, reg_type=reg_type, device_id=self.default_unit_id
            )

    def write_data(self, address, value, data_type):
        reg_type, reg_value = address
        
        if data_type in ("QX", "IX", "BOOL"):
            return self.channel.write_bit_sequence(
                address=reg_value, value=int(bool(value)), bit_count=1, device_id=self.default_unit_id, reg_type=reg_type
            )
        else:
            return self.channel.write_register_sequence(
                address=reg_value, value=int(value), reg_count=1, device_id=self.default_unit_id, reg_type=reg_type
            )

    def stop(self):
        self.channel.stop()