from openfb.resources.function_blocks.io.flogic.base.BaseOutputBlock import BaseOutputBlock

class QWStr(BaseOutputBlock):
    def __init__(self):
        super().__init__(datatype="QWStr")
    def _process_data(self, value):
        return str(value)