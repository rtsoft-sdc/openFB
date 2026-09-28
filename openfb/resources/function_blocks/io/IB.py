from openfb.resources.function_blocks.io.flogic.base.BaseInputBlock import BaseInputBlock

class IB(BaseInputBlock):
    def __init__(self):
        super().__init__(datatype="IB")
    def _process_data(self, value):
        return int(value) & 0xFF