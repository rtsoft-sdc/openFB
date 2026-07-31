from openfb.resources.function_blocks.modbus.ModbusIO import ModbusIO

class IX(ModbusIO):

    def schedule(self, event_input_name, event_input_value, QI, PARAMS):
        if event_input_name == "INIT":
            success = self._init_block(QI, PARAMS)
            if not success:
                return event_input_value, None, None, False, self.status, None
            if self.updated:
                self.updated = False
                return event_input_value, None, None, True, self.status, None
            return event_input_value, None, event_input_value, self.QO, self.status, None

        if event_input_name == "REQ":
            if not self._check_ready(QI):
                return None, event_input_value, None, False, self.status, None

            try:
                raw_val = self.channel.read_bit_sequence(
                    address=self.address,
                    bit_count=1,
                    reg_type=self.register_type,
                    device_id=self.unit_id
                )

                if raw_val is None:
                    self.status = "READ ERROR: Timeout or Invalid response"
                    return None, event_input_value, None, False, self.status, None

                in_val = bool(raw_val & 1)
                self.status = "OK"
                return None, event_input_value, None, True, self.status, in_val

            except Exception as e:
                self.status = f"REQ ERROR: {str(e)}"
                return None, event_input_value, None, False, self.status, None