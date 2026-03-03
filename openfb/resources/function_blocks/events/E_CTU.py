import logging
class E_CTU:
    def __init__(self):
        self.CV = 0
        self.Q = False

    def schedule(self, event_name, event_value, PV):
        if event_name == 'CU':
            try:
                self.CV += 1
                self.Q = (self.CV >= PV) if PV is not None else False
                return event_value, None, self.Q, self.CV
            except Exception as e:
                logging.error("Error in E_CTU: %s", str(e))
                return event_value, None, None, None

        elif event_name == 'R':
            self.CV = 0
            self.Q = False
            return None, event_value, self.Q, self.CV
    
    def __del__(self):
        logging.info('E_CTU class destroyed')
        