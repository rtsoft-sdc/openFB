import logging
class E_REND:
    def __init__(self):
        self.ei1 = False
        self.ei2 = False

    def schedule(self, event_name, event_value):
        if event_name == 'EI1':
            try:
                self.ei1 = True
            except Exception as e:
                logging.error("Error in E_REND: %s", str(e))
                return None

        elif event_name == 'EI2':
            self.ei2 = True
        elif event_name == 'R':
            self.ei1 = False
            self.ei2 = False
            return None
        if self.ei1 and self.ei2:
            self.ei1 = False
            self.ei2 = False
            return event_value
        return None
    
    def __del__(self):
        logging.info('E_REND class destroyed')