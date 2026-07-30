import logging
from pymodbus.datastore import ModbusServerContext

class ModbusSlaveChannel:
    def __init__(self, server_context: ModbusServerContext):
        self.context = server_context
        self.is_running = True
        
    def _get_slave_context(self, deviceid: int):
        return self.context[deviceid] 
        
    def _get_fx(self, reg_type):
        reg_type = reg_type.lower()
        if reg_type == "c": return 1  
        elif reg_type == "d": return 2  
        elif reg_type == "h": return 3  
        elif reg_type == "i": return 4  
        raise ValueError(f"Invalid register type {reg_type}")
    
    def read_bit_sequence(self, address: int, bit_count: int, reg_type: str, device_id: int):
        try:
            fx = self._get_fx(reg_type)
            slave_ctx = self._get_slave_context(device_id)
            bits = slave_ctx.getValues(fx, address, count=bit_count)
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
            fx = self._get_fx(reg_type)
            slave_ctx = self._get_slave_context(device_id)
            bits = [bool((value >> i) & 1) for i in range(bit_count)]
            slave_ctx.setValues(fx, address, bits)
            return True
        except Exception as e:
            logging.error(f"Error writing {reg_type} at address {address}: {e}")
            return False
            
    def read_register_sequence(self, address: int, reg_count: int, reg_type: str, device_id: int):
        try:
            slave_ctx = self._get_slave_context(device_id)
            fx = self._get_fx(reg_type)
            registers = slave_ctx.getValues(fx, address, count=reg_count)
            value = 0
            for i in range(reg_count):
                value |= (registers[i] << (16 * i))
            return value
        except Exception as e:
            logging.error(f"Error reading {reg_type} at address {address}: {e}")
            return None
        
    def write_register_sequence(self, address: int, value: int, reg_count: int, device_id: int, reg_type: str):
        try:
            fx = self._get_fx(reg_type)
            registers = [(value >> (16 * i)) & 0xFFFF for i in range(reg_count)]
            slave_ctx = self._get_slave_context(device_id)
            slave_ctx.setValues(fx, address, registers)
            return True
        except Exception as e:
            logging.error(f"Error writing {reg_type} at address {address}: {e}")
            return False
        

    def stop(self):
        pass