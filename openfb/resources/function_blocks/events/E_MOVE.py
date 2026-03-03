import logging
class E_MOVE:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                return event_value, IN
    
            except Exception as e:
                logging.error("Error in E_MOVE: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('E_MOVE class destroyed')