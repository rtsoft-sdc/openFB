import logging
class F_MAX:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            try:
                return event_value, max(IN1, IN2)
            except Exception as e:
                logging.error("Error in F_MAX: %s", str(e))
                return event_value, None
            
    def __del__(self):
        logging.info('F_MAX class destroyed')