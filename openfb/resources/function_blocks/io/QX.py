from openfb.resources.function_blocks.io.flogic.base.BaseIO import BaseIO

class QX(BaseIO):
    def __init__(self):
        super().__init__(datatype="QX")
    
    def schedule(self, event_input_name, event_input_value, QI, PARAMS, OUT):
        if event_input_name == "INIT":
            self._init_block(QI, PARAMS)
            return event_input_value, None, self.QO, self.status
        if event_input_name == "REQ":
            if not self._check_ready(QI):
                return None, event_input_value, self.QO, self.status
            bit_value = bool(OUT)
            self.execute_write(bit_value)
            return None, event_input_value, self.QO, self.status