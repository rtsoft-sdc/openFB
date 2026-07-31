from openfb.resources.function_blocks.modbus.ModbusIO import ModbusIO

class QD(ModbusIO):
   
    def schedule(self, event_input_name, event_input_value, QI, PARAMS, OUT):
        if event_input_name == "INIT":
            self._init_block(QI, PARAMS)
            return event_input_value, None, self.QO, self.status
        if event_input_name == "REQ":
            if not self._check_ready(QI):
                return event_input_value, None, self.QO, self.status
            try:
                value_32 = int(OUT) & 0xFFFFFFFF
                if self.register_type in ('c', 'd'):
                    status = self.channel.write_bit_sequence(
                        address = self.address,
                        value = value_32,
                        reg_count = 2,
                        device_id = self.unit_id,
                        reg_type = self.register_type
                    )
                else:
                    status = self.channel.write_register_sequence(
                        address = self.address,
                        value = value_32,
                        reg_count = 2,
                        device_id = self.unit_id,
                        reg_type = self.register_type
                    )
                if not status:
                    self.status = "write error"
                    return None, None, False, self.status
                self.status = "OK"
                return None, event_input_value, True, self.status
            except Exception as e:
                self.status = f"write error: {str(e)}"
                return None, None, False, self.status