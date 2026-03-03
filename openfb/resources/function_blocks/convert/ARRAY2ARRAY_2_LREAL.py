import logging
class ARRAY2ARRAY_2_LREAL:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                return event_value, [float(IN[0]), float(IN[1])]
            except Exception as e:
                logging.error("Error in ARRAY2ARRAY_2_LREAL: %s", str(e))
                return event_value, None
            
    def __del__(self):
        logging.info('ARRAY2ARRAY_2_LREAL class destroyed')