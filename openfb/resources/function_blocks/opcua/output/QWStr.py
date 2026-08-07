from openfb.resources.function_blocks.opcua.OpcUaIO import OpcUaIO

class QWStr(OpcUaIO):
    
    def schedule(self, event_input_name, event_input_value, QI, PARAMS, OUT):
        if event_input_name == "INIT":
            self._init_block(QI, PARAMS)
            return event_input_value, None, self.QO, self.status

        if event_input_name == "REQ":
            if not self._check_ready(QI):
                return None, event_input_value, self.QO, self.status
            try:
                bit_value = str(OUT)
                
                success = self.exec_io(
                    self.channel.write_value,
                    browse_path=self.browse_path,
                    value=bit_value,
                    block_type="QWStr"
                )
                
                if not success:
                    self.status = "write error"
                    return None, event_input_value, False, self.status

                self.status = "OK"
                return None, event_input_value, True, self.status

            except Exception as e:
                self.status = f"write error: {str(e)}"
                return None, event_input_value, False, self.status