from openfb.resources.function_blocks.io.AbstractChannel import AbstractChannel
from openfb.resources.function_blocks.modbus.ModbusSlaveChannel import ModbusSlaveChannel
from typing import Any
class ModbusSlaveChannelAdapter(AbstractChannel):
    
    
    def __init__(self, slave_channel: ModbusSlaveChannel, default_unitid: int = 1):
        self.channel = slave_channel
        self.default_unitid = default_unitid
        
    def read_data(self, address, datatype):
        if not address or not isinstance(address, tuple): ###
            return None
        reg_type, reg_value = address
        if datatype in ("QX", "IX", "BOOL"):
            return self.channel.read_bit_sequence(
                address=reg_value, bit_count=1, reg_type=reg_type, device_id=self.default_unitid
            )
        else:
            return self.channel.read_register_sequence(
                address=reg_value, reg_count=1, reg_type=reg_type, device_id=self.default_unitid
            )

    def write_data(self, address_params: tuple, value: Any, datatype: str) -> bool:
        if not address_params or not isinstance(address_params, tuple):
            return False
            
        reg_type, reg_value = address_params
        
        if datatype in ("QX", "IX", "BOOL"):
            return self.channel.write_bit_sequence(
                address=reg_value, value=int(bool(value)), bit_count=1, device_id=self.default_unitid, reg_type=reg_type
            )
        else:
            return self.channel.write_register_sequence(
                address=reg_value, value=int(value), reg_count=1, device_id=self.default_unitid, reg_type=reg_type
            )

    def stop(self) -> None:
        self.channel.stop()
