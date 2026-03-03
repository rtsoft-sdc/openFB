import logging
class E_D_FF:
    def __init__(self):
        self.Q = False

    def schedule(self, event_name, event_value, D):
        if event_name == 'CLK':
            try:
                self.Q = D
                return event_value, self.Q
    
            except Exception as e:
                logging.error("Error in E_D_FF: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('E_D_FF class destroyed')