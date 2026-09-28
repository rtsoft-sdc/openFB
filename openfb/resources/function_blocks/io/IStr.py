from openfb.resources.function_blocks.io.flogic.base.BaseInputBlock import BaseInputBlock

class IStr(BaseInputBlock):
    def __init__(self):
        super().__init__(datatype="IStr")
    def _process_data(self, value):
        return str(value)
