from openfb.resources.function_blocks.modbus.ModbusIO import ModbusIO

class ID(ModbusIO):
    def schedule(self, event_input_name, event_input_value, QI, PARAMS):
        if event_input_name == "INIT":
            self._init_block(QI, PARAMS)
            return event_input_value, None, self.QO, self.status, None
        if event_input_name == "REQ":
            if not self._check_ready(QI):
                return event_input_value, None, self.QO, self.status, None
            try:
                if self.register_type in ('c', 'd'):
                    value = self.channel.read_bit_sequence(
                        address = self.address,
                        bit_count = 32,
                        device_id = self.unit_id,
                        reg_type = self.register_type
                    )
                else:
                    value = self.channel.read_register_sequence(
                        address = self.address,
                        reg_count = 2,
                        device_id = self.unit_id,
                        reg_type = self.register_type
                    )
                if not value:
                    self.status = "read error"
                    return None, None, False, self.status, None
                self.status = "OK"
                value = int(value) & 0xFFFFFFFF
                return None, event_input_value, True, self.status, value
            except Exception as e:
                self.status = f"read error: {str(e)}"
                return None, None, False, self.status, None