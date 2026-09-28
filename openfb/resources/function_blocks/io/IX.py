from openfb.resources.function_blocks.io.flogic.base.BaseInputBlock import BaseInputBlock

class IX(BaseInputBlock):
    def __init__(self):
        super().__init__(datatype="IX")
    def _process_data(self, value):
        return bool(value)