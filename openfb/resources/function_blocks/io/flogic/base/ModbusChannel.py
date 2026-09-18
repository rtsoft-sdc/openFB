import logging
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
from typing import List

logger = logging.getLogger(__name__)

class ModbusChannel:
    def __init__(self, address: str, port: int = 502, timeout: float = 3.0): # if not - not
        self.address = address
        self.port = port
        self.timeout = timeout
        self.client = ModbusTcpClient(host=self.address, port=self.port, timeout=self.timeout)
        self.is_connected = False

    def _ensure_connection(self):
        if not self.is_connected or self.client is None:
            raise Exception("Not connected to Modbus server")
        
    def connect(self) -> bool:
        try:
            self.is_connected = self.client.connect()
            if not self.is_connected:
                logger.error(f"failed to connect to Modbus at {self.address}:{self.port}")
                return False
            logger.info(f"connected to Modbus at {self.address}:{self.port}")
            return True
        except ModbusException as e:
            logger.error(f"Modbus connection error: {e}")
            self.is_connected = False
            return False
        
    def disconnect(self):
        if self.client:
            self.client.close()
            self.is_connected = False
            logger.info(f"disconnected from Modbus at {self.address}:{self.port}")
    
    def read_bit_sequence(self, address:int, bit_count:int, reg_type: str, device_id: int):
        self._ensure_connection()
        try:
            if reg_type == "c":
                response = self.client.read_coils(address=address, count=bit_count, device_id=device_id)
            elif reg_type == "d":
                response = self.client.read_discrete_inputs(address=address, count=bit_count, device_id=device_id)
            else:
                raise ValueError("Invalid register type. Use 'coil' or 'discrete_input'.")
            
            if response.isError():
                logger.error(f"Error reading {reg_type} at address {address}: {response}")
                return None
            
            value = 0
            for i in range(bit_count):
                if response.bits[i]:
                    value |= (1 << i)
            return value
            
        except ModbusException as e:
            logger.error(f"Modbus read {reg_type} error: {e}")
            return None
        
    def write_bit_sequence(self, address: int, value: int, bit_count: int, device_id: int, reg_type: str) -> bool:
        self._ensure_connection()
        try:
            if bit_count == 1:
                response = self.client.write_coil(address=address, value=bool(value & 1), device_id=device_id)
            else:
                bits: List[bool] = [bool((value >> i) & 1) for i in range(bit_count)]
                response = self.client.write_coils(address=address, values=bits, device_id=device_id)
            if response.isError():
                logger.error(f"Error writing coils at address {address}: {response}")
                return False
            return True
        except ModbusException as e:
            logger.error(f"Modbus write coils error: {e}")
            return False
            
    def read_register_sequence(self, address: int, reg_count: int, reg_type: str, device_id: int):
        self._ensure_connection()
        try:
            if reg_type == "h":
                response = self.client.read_holding_registers(address=address, count=reg_count, device_id=device_id)
            elif reg_type == "i":
                response = self.client.read_input_registers(address=address, count=reg_count, device_id=device_id)
            else:
                logger.error("Invalid register type. Use 'holding' or 'input'.")
                return None
            
            value = 0
            for i in range(reg_count):
                value |= (response.registers[i] << (16 * i))
            return value

        except ModbusException as e:
            logger.error(f"Modbus read {reg_type} registers error: {e}")
            return None
        
    def write_register_sequence(self, address: int, value: int, reg_count: int, device_id: int, reg_type: str) -> bool:
        self._ensure_connection()
        try:
            if reg_count == 1:
                response = self.client.write_register(address=address, value=value, device_id=device_id)
            else:
                registers: List[int] = [(value >> (16 * i)) & 0xFFFF for i in range(reg_count)]
                response = self.client.write_registers(address=address, values=registers, device_id=device_id)            
            if response.isError():
                logger.error(f"Error writing registers at address {address}: {response}")
                return False
            return True
        except ModbusException as e:
            logger.error(f"Modbus write registers error: {e}")
            return False
            
    def stop(self):
        self.disconnect()
