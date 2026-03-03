import logging
class FB_CTU_UDINT:
    def __init__(self):
        self.cv = 0
    
    def schedule(self, event_name, event_value, CU, R, PV):
        if event_name == 'REQ':
            try:
                if R:
                    self.cv = 0
                elif CU and self.cv < 4294967295:
                    self.cv += 1
                Q = self.cv >= PV
                return event_value, Q, self.cv & 0xFFFFFFFF

            except Exception as e:
                logging.error("Error in FB_CTU_UDINT: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('FB_CTU_UDINT class destroyed')