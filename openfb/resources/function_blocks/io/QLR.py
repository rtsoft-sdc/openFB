from openfb.resources.function_blocks.io.flogic.base.BaseOutputBlock import BaseOutputBlock
class QLR(BaseOutputBlock):
    def __init__(self):
        super().__init__(datatype="QLR")
    def _process_data(self, value):
        return float(value)