import logging
class E_CTD:
    def __init__(self):
        self.CV = 0
        self.Q = False

    def schedule(self, event_name, event_value, PV):
        if event_name == 'CD':
            try:
                if self.CV > 0:
                    self.CV -= 1
                self.Q = (self.CV == 0)
                return event_value, None, self.Q, self.CV
            except Exception as e:
                logging.error("Error in E_CTD: %s", str(e))
                return event_value, None, None, None

        elif event_name == 'LD':
            self.CV = PV
            self.Q = (self.CV == 0)
            return None, event_value, self.Q, self.CV
    
    def __del__(self):
        logging.info('E_CTD class destroyed')