from openfb.resources.function_blocks.io.flogic.base.BaseOutputBlock import BaseOutputBlock
class QB(BaseOutputBlock):
    def __init__(self):
        super().__init__(datatype="QB")
    def _process_data(self, value):
        return int(value) & 0xFF