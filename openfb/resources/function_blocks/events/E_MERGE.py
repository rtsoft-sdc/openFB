import logging
class E_MERGE:
    def schedule(self, event_name, event_value):
        if event_name in ['EI1', 'EI2']:
            try:
                return event_value
    
            except Exception as e:
                logging.error("Error in E_MERGE: %s", str(e))
                return None
    def __del__(self):
        logging.info('E_MERGE class destroyed')