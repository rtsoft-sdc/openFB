import logging
class FB_CTD_ULINT:
    def __init__(self):
        self.cv = 0
    
    def schedule(self, event_name, event_value, CD, PV, LD):
        if event_name == 'REQ':
            try:
                if LD:
                    self.cv = PV & 0xFFFFFFFFFFFFFFFF
                elif CD and self.cv > 0:
                    self.cv -= 1
                Q = self.cv <= 0
                return event_value, Q, self.cv & 0xFFFFFFFFFFFFFFFF

            except Exception as e:
                logging.error("Error in FB_CTD_ULINT: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('FB_CTD_ULINT class destroyed')