import logging
class OF_E_R_TRIG:
    def __init__(self):
        self.last = False

    def schedule(self, event_name, event_value, QI):
        if event_name == 'EI':
            try:
                if QI and not self.last:
                    self.last = QI
                    return event_value, None
                self.last = QI
    
            except Exception as e:
                logging.error("Error in E_R_TRIG: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('OF_E_R_TRIG class destroyed')