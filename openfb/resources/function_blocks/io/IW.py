from openfb.resources.function_blocks.io.flogic.base.BaseInputBlock import BaseInputBlock

class IW(BaseInputBlock):
    def __init__(self):
        super().__init__(datatype="IW")
    def _process_data(self, value):
        return int(value) & 0xFFFF