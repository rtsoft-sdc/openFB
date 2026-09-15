from openfb.resources.function_blocks.modbus.ModbusIO import ModbusIO

class QX(ModbusIO): 
    
    def schedule(self, event_input_name, event_input_value, QI, PARAMS, OUT):
        if event_input_name == "INIT":
            self._init_block(QI, PARAMS)
            return event_input_value, None, self.QO, self.status
        if event_input_name == "REQ":
            if not self._check_ready(QI):
                return None, event_input_value, self.QO, self.status
            try:
                bit_value = bool(OUT)
                try:
                    success = self.exec_io(
                        self.channel.write_bit_sequence,
                        address=self.register_value,
                        value=bit_value,
                        bit_count=1,
                        device_id=self.unit_id,
                        reg_type=self.register_type
                    )
                except Exception as e:
                    self.status = f"write error: {str(e)}"
                    return None, event_input_value, False, self.status
                self.status = "OK"
                return None, event_input_value, True, self.status
            except Exception as e:
                self.status = f"write error: {str(e)}"
                return None, event_input_value, False, self.status
                