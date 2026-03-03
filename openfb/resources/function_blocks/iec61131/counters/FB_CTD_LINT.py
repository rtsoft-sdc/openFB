import logging
class FB_CTD_LINT:
    def __init__(self):
        self.cv = 0
    
    def schedule(self, event_name, event_value, CD, PV, LD):
        if event_name == 'REQ':
            try:
                if LD:
                    self.cv = PV
                elif CD and self.cv > -9223372036854775808:
                    self.cv -= 1
                Q = self.cv <= 0
                return event_value, Q, self.cv

            except Exception as e:
                logging.error("Error in FB_CTD_LINT: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('FB_CTD_LINT class destroyed')