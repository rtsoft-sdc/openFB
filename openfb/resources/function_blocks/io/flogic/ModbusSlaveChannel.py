import logging
from pymodbus.datastore import ModbusServerContext

logger = logging.getLogger(__name__)

class ModbusSlaveChannel:
    def __init__(self, server_context: ModbusServerContext):
        self.context = server_context
        self.is_running = True
        self._type_idx_map = {'c': 0, 'd': 1, 'h': 2, 'i': 3}

    def _get_slave_context(self, deviceid: int):
        try:
            return self.context._devices[deviceid]
        except KeyError:
            try:
                return self.context._devices[0]
            except Exception:
                logger.error(f"Device ID {deviceid} not found in context")
                return None

    def _get_sim_entry(self, slave_ctx, reg_type: str):
        """Вспомогательный метод получения нужного SimData блока из SimDevice."""
        idx = self._type_idx_map.get(reg_type, 2)
        simdevice = getattr(slave_ctx, 'simdevice', None)
        if not simdevice or not hasattr(simdevice, 'simdata'):
            return None
        
        simdata_group = simdevice.simdata[idx]
        if isinstance(simdata_group, (list, tuple)) and len(simdata_group) > 0:
            return simdata_group[0]
        return simdata_group

    def _read_values_from_store(self, slave_ctx, reg_type: str, address: int, count: int):
        entry = self._get_sim_entry(slave_ctx, reg_type)
        if not entry or not hasattr(entry, 'values'):
            return None
        
        base_addr = getattr(entry, 'address', 0)
        offset = address - base_addr
        if offset < 0:
            offset = address

        return entry.values[offset : offset + count]

    def _write_values_to_store(self, slave_ctx, reg_type: str, address: int, values: list) -> bool:
        entry = self._get_sim_entry(slave_ctx, reg_type)
        if not entry or not hasattr(entry, 'values'):
            return False

        base_addr = getattr(entry, 'address', 0)
        offset = address - base_addr
        if offset < 0:
            offset = address

        for i, val in enumerate(values):
            idx = offset + i
            if idx < len(entry.values):
                entry.values[idx] = val
            else:
                entry.values.extend([0] * (idx - len(entry.values))) # extend address
                entry.values.append(val)
        return True

    def read_bit_sequence(self, address: int, bit_count: int, reg_type: str, device_id: int):
        try:
            slave_ctx = self._get_slave_context(device_id)
            if not slave_ctx:
                return None

            bits = self._read_values_from_store(slave_ctx, reg_type, address, bit_count)
            if bits is None or len(bits) < bit_count:
                return None

            value = 0
            for i in range(bit_count):
                if bits[i]:
                    value |= (1 << i)
            return value
        except Exception as e:
            logger.error(f"Error reading bit sequence at {reg_type} {address}: {e}")
            return None

    def write_bit_sequence(self, address: int, value: int, bit_count: int, device_id: int, reg_type: str) -> bool:
        try:
            slave_ctx = self._get_slave_context(device_id)
            if not slave_ctx:
                return False

            bits = [bool((value >> i) & 1) for i in range(bit_count)]
            return self._write_values_to_store(slave_ctx, reg_type, address, bits)
        except Exception as e:
            logger.error(f"Error writing bit sequence at {reg_type} address {address}: {e}")
            return False

    def read_register_sequence(self, address: int, reg_count: int, reg_type: str, device_id: int):
        try:
            slave_ctx = self._get_slave_context(device_id)
            if not slave_ctx:
                return None

            registers = self._read_values_from_store(slave_ctx, reg_type, address, reg_count)
            if registers is None or len(registers) < reg_count:
                return None

            value = 0
            for i in range(reg_count):
                value |= (int(registers[i]) << (16 * i))
            return value
        except Exception as e:
            logger.error(f"Error reading register sequence at {reg_type} {address}: {e}")
            return None

    def write_register_sequence(self, address: int, value: int, reg_count: int, device_id: int, reg_type: str) -> bool:
        try:
            slave_ctx = self._get_slave_context(device_id)
            if not slave_ctx:
                return False

            registers = [(value >> (16 * i)) & 0xFFFF for i in range(reg_count)]
            return self._write_values_to_store(slave_ctx, reg_type, address, registers)
        except Exception as e:
            logger.error(f"Error writing register sequence at {reg_type} address {address}: {e}")
            return False

    def stop(self):
        self.is_running = False