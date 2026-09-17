from openfb.resources.function_blocks.io.flogic.base.BaseIO import BaseIO

class QD(BaseIO):
    def __init__(self):
        super().__init__(datatype="QD")
    
    def schedule(self, event_input_name, event_input_value, QI, PARAMS, OUT):
        if event_input_name == "INIT":
            self._init_block(QI, PARAMS)
            return event_input_value, None, self.QO, self.status
        if event_input_name == "REQ":
            if not self._check_ready(QI):
                return None, event_input_value, self.QO, self.status
            value_32 = int(OUT) & 0xFFFFFFFF
            value = self.execute_write(value_32)
            return None, event_input_value, self.QO, self.status