from openfb.resources.function_blocks.modbus import ModbusIO

class IX(ModbusIO):

    def schedule(self, event_input_name, event_input_value, QI, PARAMS):
        if event_input_name == "INIT":
            success = self._init_block(QI, PARAMS)
            return event_input_value, None, self.QO, self.STATUS, False

        if event_input_name == "REQ":
            if not self._check_ready(QI):
                return None, None, False, self.STATUS, False

            try:
                raw_val = self.channel.read_bit_sequence(
                    address=self.address,
                    bit_count=1,
                    reg_type=self.register_type,
                    device_id=self.unit_id
                )

                if raw_val is None:
                    self.STATUS = "READ ERROR: Timeout or Invalid response"
                    return None, None, False, self.STATUS, False

                in_val = bool(raw_val & 1)
                self.STATUS = "OK"
                return None, event_input_value, True, self.STATUS, in_val

            except Exception as e:
                self.STATUS = f"REQ ERROR: {str(e)}"
                return None, None, False, self.STATUS, False