from openfb.resources.function_blocks.io.flogic.base.BaseIO import BaseIO

class BaseInputBlock(BaseIO):
    def __init__(self, datatype: str):
        super().__init__(datatype=datatype)

    def schedule(self, event_input_name, event_input_value, QI, PARAMS):
        if event_input_name == "INIT":
            self._init_block(QI, PARAMS)
            return event_input_value, None, None, self.QO, self.status, None
        
        if event_input_name == "REQ":
            if not self._check_ready(QI):
                return None, event_input_value, None, self.QO, self.status, None        
            raw_value = self.execute_read()
            try:
                value = self._process_data(raw_value)
            except (ValueError, TypeError):
                value = None
            return None, event_input_value, None, self.QO, self.status, value
        
        return None, None, None, self.QO, self.status, None