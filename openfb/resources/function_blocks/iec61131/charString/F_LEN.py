import logging
class F_LEN:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                return event_value, len(IN)
 
            except Exception as e:
                logging.error("Error in F_LEN: %s", str(e))
                return event_value, None
            
    def __del__(self):
        logging.info('F_LEN class destroyed')
