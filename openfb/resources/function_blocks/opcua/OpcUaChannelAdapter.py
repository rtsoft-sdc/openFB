from openfb.resources.function_blocks.protocol.AbstractChannel import AbstractChannel
from openfb.resources.function_blocks.opcua.OpcuaMasterChannel import OpcUaMasterChannel


class OpcUaChannelAdapter(AbstractChannel):
    def __init__(self, master_channel: OpcUaMasterChannel):
        self.channel = master_channel
        
    def read_data(self, address, datatype):
        browse_path = str(address)
        return self.channel.read_value(browse_path=browse_path, block_type=datatype)
    
    def write_data(self, address, value, datatype):
        browse_path = str(address)
        return self.channel.write_value(browse_path=browse_path, value=value, block_type=datatype)
    
    def stop(self):
        self.channel.stop()