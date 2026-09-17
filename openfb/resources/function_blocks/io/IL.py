from openfb.resources.function_blocks.io.flogic.base.BaseInputBlock import BaseInputBlock

class IL(BaseInputBlock):
    def __init__(self):
        super().__init__(datatype="IL")
    def _process_data(self, value):
        return int(value) & 0xFFFFFFFFFFFFFFFF