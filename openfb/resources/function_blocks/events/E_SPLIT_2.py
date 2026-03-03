import logging
class E_SPLIT_2:
    def schedule(self, event_name, event_value):
        if event_name == 'EI':
            try:
                return [event_value, event_value]
    
            except Exception as e:
                logging.error("Error in E_SPLIT_2: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('E_SPLIT_2 class destroyed')