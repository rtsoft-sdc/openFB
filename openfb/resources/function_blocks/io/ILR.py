from openfb.resources.function_blocks.io.flogic.base.BaseInputBlock import BaseInputBlock

class ILR(BaseInputBlock):
    def __init__(self):
        super().__init__(datatype="ILR")
    def _process_data(self, value):
        return float(value)
