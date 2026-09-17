from openfb.resources.function_blocks.io.flogic.base.BaseInputBlock import BaseInputBlock

class ID(BaseInputBlock):
    def __init__(self):
        super().__init__(datatype="ID")
    def _process_data(self, value):
        return int(value) & 0xFFFFFFFF