import logging
class E_T_FF:
    def __init__(self):
        self.Q = False

    def schedule(self, event_name, event_value):
        if event_name == 'CLK':
            try:
                self.Q = not self.Q
                return event_value, self.Q
    
            except Exception as e:
                logging.error("Error in E_T_FF: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('E_T_FF class destroyed')