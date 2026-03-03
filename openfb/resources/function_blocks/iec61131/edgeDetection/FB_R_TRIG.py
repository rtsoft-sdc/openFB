import logging
class FB_R_TRIG:
    def __init__(self):
        self.mem = False 
    
    def schedule(self, event_name, event_value, CLK):
        if event_name == 'REQ':
            try:
                Q = CLK and (not self.mem)
                self.mem = CLK
                return event_value, Q

            except Exception as e:
                logging.error("Error in FB_R_TRIG: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('FB_R_TRIG class destroyed')