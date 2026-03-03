import logging
class E_RS:
    def __init__(self):
        self.Q = False

    def schedule(self, event_name, event_value):
        if event_name == 'S':
            try:
                self.Q = True
                return event_value, self.Q
            except Exception as e:
                logging.error("Error in E_RS: %s", str(e))
                return event_value, None

        elif event_name == 'R':
            self.Q = False
            return event_value, self.Q
        return None
    
    def __del__(self):
        logging.info('E_RS class destroyed')