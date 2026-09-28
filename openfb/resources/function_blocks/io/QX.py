from openfb.resources.function_blocks.io.flogic.base.BaseOutputBlock import BaseOutputBlock

class QX(BaseOutputBlock):
    def __init__(self):
        super().__init__(datatype="QX")
    def _process_data(self, value):
        return bool(value)