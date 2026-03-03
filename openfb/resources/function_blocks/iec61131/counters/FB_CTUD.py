import logging
class FB_CTUD:
    def __init__(self):
        self.cv = 0
    
    def schedule(self, event_name, event_value, CU, CD, R, LD, PV):
        if event_name == 'REQ':
            try:
                if R:
                    self.cv = 0
                elif LD:
                    self.cv = PV
                elif not (CU and CD):
                    if CU and self.cv < 32767:
                        self.cv += 1
                    elif CD and self.cv > -32768:
                        self.cv -= 1
            
                QU = self.cv >= PV
                QD = self.cv <= 0
                return event_value, QU, QD, self.cv

            except Exception as e:
                logging.error("Error in FB_CTUD: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('FB_CTUD class destroyed')