import logging
from openfb.resources.function_blocks.io.flogic.base.utils import normalize_fb_id

class BaseProtocolFB:
    def __init__(self):
        self.status = "CREATED"
        self.channel = None
        self.adapter = None
        self.fb_registry = None
        self.fb_name = ""
        self.fb_prefix = ""
        
    def set_fb_registry_and_name(self, fb_registry, fb_name):
        self.fb_registry = fb_registry
        self.fb_name = str(fb_name)
        self.fb_prefix = self.fb_name.rpartition('.')[0] + "."
        
    def _find_fb_object(self, ioblock_id):
        if not self.fb_registry:
            return None
        targetid = self.fb_prefix + normalize_fb_id(ioblock_id)
        if not targetid:
            return None
        for val in self.fb_registry.values():
            fb_name = getattr(val, "fb_name", '')
            if fb_name == targetid:
                return getattr(val, 'fb_obj', None)
        return None
    
    def bind_and_connect_channels(self, *io_list):
        for io_block in io_list[0]:
            if not io_block:
                continue
            fb_obj = self._find_fb_object(io_block)
            if fb_obj and hasattr(fb_obj, 'bind_channel'):
                try:
                    fb_obj.bind_channel(self.adapter)
                except Exception as e:
                    logging.error(f"OpcUA error:{e}")
        self.status = "OK"
    
    def stop_channel(self):
        if self.adapter:
            try:
                self.adapter.stop()
            except Exception as e:
                logging.error(f"Error stopping adapter: {e}")
            self.adapter = None
            
        if self.channel:
            try:
                if hasattr(self.channel, 'stop'):
                    self.channel.stop()
            except Exception as e:
                logging.error(f"Error stopping channel: {e}")
            self.channel = None
            
        self.status = "STOPPED"
    
    def __del__(self):
        self.stop_channel()