import logging
from pymodbus.datastore import ModbusServerContext

class ModbusSlaveChannel:
    def __init__(self, server_context: ModbusServerContext):
        self.context = server_context
        self.is_running = True
        self._fx_map = {
            'c': (1, 15), # coils
            'd': (2, None), # discrete inputs
            'h': (3, 16), # holding registers
            'i': (4, None) # input registers
        }
        
    def _get_slave_context(self, deviceid: int):
        try:
            return self.context._devices[deviceid]
        except KeyError:
            try:
                return self.context._devices[0]
            except Exception:
                logging.error(f"Device ID {deviceid} not found in context")
                return None          
    
    def read_bit_sequence(self, address: int, bit_count: int, reg_type: str, device_id: int):
        try:
            slave_ctx = self._get_slave_context(device_id)
            if not slave_ctx:
                return None
            read_fx = self._fx_map.get(reg_type, (1, None))[0]
            bits = slave_ctx.getValues(read_fx, address, count=bit_count)
            
            value = 0
            for i in range(bit_count):
                if bits[i]:
                    value |= (1 << i)
            return value
        except Exception as e:
            logging.error(f"Error reading at {reg_type} {address}: {e}")
            return False
            
    def write_bit_sequence(self, address: int, value: int, bit_count: int, device_id: int, reg_type: str):
        try:
            slave_ctx = self._get_slave_context(device_id)
            if not slave_ctx:
                return None
            write_fx = self._fx_map.get(reg_type, (1, 15))[1] or 15
            bits = [bool((value >> i) & 1) for i in range(bit_count)]
            slave_ctx.setValues(write_fx, address, bits)
            return True
        except Exception as e:
            logging.error(f"Error writing {reg_type} at address {address}: {e}")
            return False
            
    def read_register_sequence(self, address: int, reg_count: int, reg_type: str, device_id: int):
        try:
            slave_ctx = self._get_slave_context(device_id)
            if not slave_ctx:
                return None
            read_fx = self._fx_map.get(reg_type, (3, None))[0]
            registers = slave_ctx.getValues(read_fx, address, count=reg_count)
            value = 0
            for i in range(reg_count):
                value |= (registers[i] << (16 * i))
            return value
        except Exception as e:
            logging.error(f"Error reading {reg_type} at address {address}: {e}")
            return False
        
    def write_register_sequence(self, address: int, value: int, reg_count: int, device_id: int, reg_type: str):
        try:
            slave_ctx = self._get_slave_context(device_id)
            if not slave_ctx:
                return None
            registers = [(value >> (16 * i)) & 0xFFFF for i in range(reg_count)]
            write_fx = self._fx_map.get(reg_type, (1, 15))[1] or 15
            slave_ctx.setValues(write_fx, address, registers)
            return True
        except Exception as e:
            logging.error(f"Error writing {reg_type} at address {address}: {e}")
            return False
        

    def stop(self):
        pass