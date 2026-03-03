import logging
class E_MERGE_4:
    def schedule(self, event_name, event_value):
        if event_name in ['EI1', 'EI2', 'EI3', 'EI4']:
            try:
                return event_value
    
            except Exception as e:
                logging.error("Error in E_MERGE_4: %s", str(e))
                return None
    def __del__(self):
        logging.info('E_MERGE_4 class destroyed')