from openfb.resources.function_blocks.io.AbstractChannel import AbstractChannel
from openfb.resources.function_blocks.io.flogic.ModbusChannel import ModbusChannel
from openfb.resources.function_blocks.io.flogic.utils import get_addr_update_delay_mode, parse_register_value

class ModbusChannelAdapter(AbstractChannel):
    def __init__(self, modbus_channel: ModbusChannel, default_unitid: int = 1):
        self.channel = modbus_channel
        self.default_unitid = default_unitid
        
    def parse_IO_params(self, params):
        address, update_interval, delay, mode, status = get_addr_update_delay_mode(params)
        if address is None:
            address = params
        return address, update_interval, delay, mode, status
        
    def read_data(self, address, datatype):
        reg_type, reg_value = parse_register_value(address)
        if datatype in ("QX", "IX", "BOOL"):
            return self.channel.read_bit_sequence(
                address=reg_value, bit_count=1, reg_type=reg_type, device_id=self.default_unitid
            )
        else:
            return self.channel.read_register_sequence(
                address=reg_value, reg_count=1, reg_type=reg_type, device_id=self.default_unitid
            )

    def write_data(self, address, value, data_type):
        reg_type, reg_value = parse_register_value(address)
        
        if data_type in ("QX", "IX", "BOOL"):
            return self.channel.write_bit_sequence(
                address=reg_value, value=int(bool(value)), bit_count=1, device_id=self.default_unitid, reg_type=reg_type
            )
        else:
            return self.channel.write_register_sequence(
                address=reg_value, value=int(value), reg_count=1, device_id=self.default_unitid, reg_type=reg_type
            )

    def stop(self):
        self.channel.stop()