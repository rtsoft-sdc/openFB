import logging
class F_NOT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                return event_value, ~int(IN)

            except Exception as e:
                logging.error("Error in F_NOT: %s", str(e))
                return event_value, None
            
    def __del__(self):
        logging.info('F_NOT class destroyed')
