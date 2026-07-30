from openfb.resources.function_blocks.modbus.ModbusIO import ModbusIO

class IW(ModbusIO):

    def schedule(self, event_input_name, event_input_value, QI, PARAMS):
        if event_input_name == "INIT":
            self._init_block(QI, PARAMS)
            return event_input_value, None, self.QO, self.STATUS, 0

        if event_input_name == "REQ":
            if not self._check_ready(QI):
                return None, None, False, self.STATUS, 0

            try:
                rt = self.register_type.lower()

                if rt in ('c', 'd'):
                    raw_val = self.channel.read_bit_sequence(
                        address=self.address,
                        bit_count=16,
                        reg_type=self.register_type,
                        device_id=self.unit_id
                    )
                else:
                    raw_val = self.channel.read_register_sequence(
                        address=self.address,
                        reg_count=1,
                        reg_type=self.register_type,
                        device_id=self.unit_id
                    )

                if raw_val is None:
                    self.STATUS = "READ ERROR: No response or invalid address"
                    return None, None, False, self.STATUS, 0

                in_val = int(raw_val) & 0xFFFF
                self.STATUS = "OK"
                return None, event_input_value, True, self.STATUS, in_val

            except Exception as e:
                self.STATUS = f"REQ ERROR: {str(e)}"
                return None, None, False, self.STATUS, 0