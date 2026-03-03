import logging
class F_SHL:
    def schedule(self, event_name, event_value, IN, N):
        if event_name == 'REQ':
            try:
                return event_value, int(IN) << int(N)

            except Exception as e:
                logging.error("Error in F_SHL: %s", str(e))
                return event_value, None
            
    def __del__(self):
        logging.info('F_SHL class destroyed')
