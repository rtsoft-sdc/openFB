from openfb.resources.function_blocks.io.flogic.base.BaseOutputBlock import BaseOutputBlock
class QR(BaseOutputBlock):
    def __init__(self):
        super().__init__(datatype="QR")
    def _process_data(self, value):
        return float(value)