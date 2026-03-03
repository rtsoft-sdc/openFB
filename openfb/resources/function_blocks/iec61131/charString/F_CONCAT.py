import logging
class F_CONCAT:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            try:
                a = '' if IN1 is None else str(IN1)
                b = '' if IN2 is None else str(IN2)
                return event_value, a + b

            except Exception as e:
                logging.error("Error in F_CONCAT: %s", str(e))
                return event_value, None
            
    def __del__(self):
        logging.info('F_CONCAT class destroyed')
