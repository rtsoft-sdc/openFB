import logging
class FB_CTU:
    def __init__(self):
        self.cv = 0
    
    def schedule(self, event_name, event_value, CU, R, PV):
        if event_name == 'REQ':
            try:
                if R:
                    self.cv = 0
                elif CU and self.cv < 32767:
                    self.cv += 1
                Q = self.cv >= PV
                return event_value, Q, self.cv

            except Exception as e:
                logging.error("Error in FB_CTU: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('FB_CTU class destroyed')
        