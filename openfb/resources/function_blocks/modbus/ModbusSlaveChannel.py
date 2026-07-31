import logging
from pymodbus.datastore import ModbusServerContext

class ModbusSlaveChannel:
    def __init__(self, server_context: ModbusServerContext):
        self.context = server_context
        self.is_running = True
        self._types_index = {
            'c': 0,
            'd': 1,
            'h': 2,
            'i': 3
        }
        
    def _get_slave_context(self, deviceid: int):
        try:
            if deviceid in self.context._devices:
                return self.context._devices[deviceid]
            if 0 in self.context._devices:
                return self.context._devices[0]
            logging.error(f"Device ID {deviceid} not found in context")
            return None
        except Exception as e:
            logging.error(f"Error retrieving slave context for device ID {deviceid}: {e}")
            return None
    
    def _get_simdata_address(self, slave_ctx, reg_type: str):
        idx = self._types_index.get(reg_type)
        simdata_list = slave_ctx.simdevice.simdata[idx]
        return simdata_list[0]
    
    def read_bit_sequence(self, address: int, bit_count: int, reg_type: str, device_id: int):
        try:
            slave_ctx = self._get_slave_context(device_id)
            entry = self._get_simdata_address(slave_ctx, reg_type)
            offset = address - getattr(entry, 'address', 0)
            bits = entry.values[offset:offset + bit_count]
            
            value = 0
            for i in range(bit_count):
                if bits[i]:
                    value |= (1 << i)
            return value
        except Exception as e:
            logging.error(f"Error reading {reg_type} at address {address}: {e}")
            return None
            
    def write_bit_sequence(self, address: int, value: int, bit_count: int, device_id: int, reg_type: str):
        try:
            slave_ctx = self._get_slave_context(device_id)
            bits = [bool((value >> i) & 1) for i in range(bit_count)]
            entry = self._get_simdata_address(slave_ctx, reg_type)
            offset = address - getattr(entry, 'address', 0)
            entry.values[offset:offset + bit_count] = bits
            return True
        except Exception as e:
            logging.error(f"Error writing {reg_type} at address {address}: {e}")
            return False
            
    def read_register_sequence(self, address: int, reg_count: int, reg_type: str, device_id: int):
        try:
            slave_ctx = self._get_slave_context(device_id)
            entry = self._get_simdata_address(slave_ctx, reg_type)
            offset = address - getattr(entry, 'address', 0)
            registers = entry.values[offset:offset + reg_count]
            value = 0
            for i in range(reg_count):
                value |= (registers[i] << (16 * i))
            return value
        except Exception as e:
            logging.error(f"Error reading {reg_type} at address {address}: {e}")
            return None
        
    def write_register_sequence(self, address: int, value: int, reg_count: int, device_id: int, reg_type: str):
        try:
            slave_ctx = self._get_slave_context(device_id)
            registers = [(value >> (16 * i)) & 0xFFFF for i in range(reg_count)]
            entry = self._get_simdata_address(slave_ctx, reg_type)
            offset = address - getattr(entry, 'address', 0)
            entry.values[offset:offset + reg_count] = registers
            return True
        except Exception as e:
            logging.error(f"Error writing {reg_type} at address {address}: {e}")
            return False
        

    def stop(self):
        pass