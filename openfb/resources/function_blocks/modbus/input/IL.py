from openfb.resources.function_blocks.modbus.ModbusIO import ModbusIO

class IL(ModbusIO):
    def schedule(self, event_input_name, event_input_value, QI, PARAMS):
        if event_input_name == "INIT":
            success = self._init_block(QI, PARAMS)
            if not success:
                return event_input_value, None, None, None, False, self.status
            if self.updated:
                self.updated = False
                return event_input_value, None, event_input_value, True, self.status, None
            return event_input_value, None, None, self.QO, self.status, None
        if event_input_name == "REQ":
            if not self._check_ready(QI):
                return event_input_value, None, None, self.QO, self.status, None
            try:
                if self.register_type in ('c', 'd'):
                    value = self.exec_io(
                        self.channel.read_bit_sequence,
                        address = self.register_value,
                        bit_count = 64,
                        device_id = self.unit_id,
                        reg_type = self.register_type
                    )
                else:
                    value = self.exec_io(
                        self.channel.read_register_sequence,
                        address = self.register_value,
                        reg_count = 4,
                        device_id = self.unit_id,
                        reg_type = self.register_type
                    )
                if not value:
                    self.status = "read error"
                    return None, event_input_value, None, False, self.status, None
                value = int(value) & 0xFFFFFFFFFFFFFFFF
                
                self.status = "OK"
                return None, event_input_value, None, True, self.status, value
            except Exception as e:
                self.status = f"read error: {str(e)}"
                return event_input_value, None, None, False, self.status, None
