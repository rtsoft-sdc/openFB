from openfb.resources.function_blocks.io.flogic.base.BaseOutputBlock import BaseOutputBlock

class QW(BaseOutputBlock):
    def __init__(self):
        super().__init__(datatype="QW")
    def _process_data(self, value):
        return int(value) & 0xFFFF