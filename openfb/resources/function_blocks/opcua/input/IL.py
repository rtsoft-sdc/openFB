from openfb.resources.function_blocks.opcua.OpcUaIO import OpcUaIO

class IL(OpcUaIO):
    
    def schedule(self, event_input_name, event_input_value, QI, PARAMS):
        if event_input_name == "INIT":
            success = self._init_block(QI, PARAMS)
            if not success:
                return event_input_value, None, None, False, self.status, None
            if self.updated:
                self.updated = False
                return event_input_value, None, event_input_value, True, self.status, None
            return event_input_value, None, None, self.QO, self.status, None

        if event_input_name == "REQ":
            if not self._check_ready(QI):
                return None, event_input_value, None, self.QO, self.status, None
            try:
                value = self.exec_io(
                    self.channel.read_value,
                    browse_path=self.browse_path,
                    block_type="IL"
                )

                if value is None or value is False and isinstance(value, bool):
                    self.status = "read error"
                    return None, event_input_value, None, False, self.status, None

                self.status = "OK"

                value = int(value) & 0xFFFFFFFFFFFFFFFF
                return None, event_input_value, None, True, self.status, value

            except Exception as e:
                self.status = f"read error: {str(e)}"
                return None, event_input_value, None, False, self.status, None