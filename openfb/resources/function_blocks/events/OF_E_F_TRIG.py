import logging
class E_F_TRIG:
    def __init__(self):
        self.last = False

    def schedule(self, event_name, event_value, QI):
        if event_name == 'EI':
            try:
                if not QI and self.last:
                    self.last = QI
                    return event_value
                self.last = QI
        
            except Exception as e:
                logging.error("Error in E_F_TRIG: %s", str(e))
                return None
    def __del__(self):
        logging.info('E_F_TRIG class destroyed')