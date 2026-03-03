import logging
class E_PERMIT:
    def schedule(self, event_name, event_value, PERMIT):
        if event_name == 'EI' and PERMIT:
            try:
                return event_value
    
            except Exception as e:
                logging.error("Error in E_PERMIT: %s", str(e))
                return None
    def __del__(self):
        logging.info('E_PERMIT class destroyed')