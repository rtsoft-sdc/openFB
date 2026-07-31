from openfb.resources.function_blocks.modbus.ModbusIO import ModbusIO

class QW(ModbusIO):

    def schedule(self, event_input_name, event_input_value, QI, PARAMS, OUT):
        if event_input_name == "INIT":
            self._init_block(QI, PARAMS)
            return event_input_value, None, self.QO, self.status

        if event_input_name == "REQ":
            if not self._check_ready(QI):
                return None, None, False, self.status

            try:
                word_val = int(OUT) & 0xFFFF
                rt = self.register_type.lower()

                if rt in ('c', 'd'):
                    success = self.channel.write_bit_sequence(
                        address=self.address,
                        value=word_val,
                        bit_count=16,
                        reg_type=self.register_type,
                        device_id=self.unit_id
                    )
                else:
                    success = self.channel.write_register_sequence(
                        address=self.address,
                        value=word_val,
                        reg_count=1,
                        reg_type=self.register_type,
                        device_id=self.unit_id
                    )

                if not success:
                    self.status = "WRITE ERROR: Failed to write register"
                    return None, None, False, self.status

                self.status = "OK"
                return None, event_input_value, True, self.status

            except Exception as e:
                self.status = f"REQ ERROR: {str(e)}"
                return None, None, False, self.status