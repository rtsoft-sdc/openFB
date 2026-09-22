from openfb.resources.function_blocks.io.flogic.base.AbstractChannel import AbstractChannel
from openfb.resources.function_blocks.io.flogic.base.OpcuaChannel import OpcUaChannel

class OpcUaChannelAdapter(AbstractChannel):
    def __init__(self, master_channel: OpcUaChannel):
        self.channel = master_channel
        
    def parse_IO_params(self, params):
        address = str(params).strip().strip("'\"") if params else None
        if address is None:
            address = params
        return address, 0.0, 0.0, "req", "OK"
        
    def read_data(self, address, datatype):
        browse_path = str(address)
        return self.channel.read_value(browse_path=browse_path, block_type=datatype)
    
    def write_data(self, address, value, datatype):
        browse_path = str(address)
        return self.channel.write_value(browse_path=browse_path, value=value, block_type=datatype)
    
    def stop(self):
        self.channel.stop()