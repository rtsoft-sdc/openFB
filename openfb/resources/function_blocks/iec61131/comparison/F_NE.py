import logging
class F_NE:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            try:
                return event_value, IN1 != IN2

            except Exception as e:
                logging.error("Error in F_NE: %s", str(e))
                return event_value, None
            
    def __del__(self):
        logging.info('F_NE class destroyed')
