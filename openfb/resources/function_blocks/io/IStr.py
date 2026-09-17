from openfb.resources.function_blocks.io.flogic.base.BaseIO import BaseIO

class IStr(BaseIO):
    def __init__(self):
        super().__init__(datatype="IStr")
    
    def schedule(self, event_input_name, event_input_value, QI, PARAMS):
        if event_input_name == "INIT":
            self._init_block(QI, PARAMS)
            return event_input_value, None, None, self.QO, self.status, None
        if event_input_name == "REQ":
            if not self._check_ready(QI):
                return None, event_input_value, None, self.QO, self.status, None
            value = self.execute_read()
            value = str(value) 
            return None, event_input_value, None, self.QO, self.status, value