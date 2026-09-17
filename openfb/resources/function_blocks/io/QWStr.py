from openfb.resources.function_blocks.io.flogic.base.BaseIO import BaseIO

class QWStr(BaseIO):
    def __init__(self):
        super().__init__(datatype="QWStr")
    
    def schedule(self, event_input_name, event_input_value, QI, PARAMS, OUT):
        if event_input_name == "INIT":
            self._init_block(QI, PARAMS)
            return event_input_value, None, self.QO, self.status

        if event_input_name == "REQ":
            if not self._check_ready(QI):
                return None, event_input_value, self.QO, self.status
            str_value = str(OUT) if OUT is not None else ""
            value = self.execute_write(str_value)
            return None, event_input_value, self.QO, self.status