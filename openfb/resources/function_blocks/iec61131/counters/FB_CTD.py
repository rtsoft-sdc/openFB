import logging
class FB_CTD:
    def __init__(self):
        self.cv = 0
    
    def schedule(self, event_name, event_value, CD, LD, PV):
        if event_name == 'REQ':
            try:
                if LD:
                    self.cv = PV
                elif CD and self.cv > -32768:
                    self.cv -= 1
                Q = self.cv <= 0
                return event_value, Q, self.cv

            except Exception as e:
                logging.error("Error in FB_CTD: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('FB_CTD class destroyed')