import logging
class FB_F_TRIG:
    def __init__(self):
        self.mem = True
    
    def schedule(self, event_name, event_value, CLK):
        if event_name == 'REQ':
            try:
                Q = (not CLK) and (not self.mem)
                self.mem = not CLK
                return event_value, Q

            except Exception as e:
                logging.error("Error in FB_F_TRIG: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('FB_F_TRIG class destroyed')