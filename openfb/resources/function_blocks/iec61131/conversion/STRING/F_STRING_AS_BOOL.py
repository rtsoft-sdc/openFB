import logging
class F_STRING_AS_BOOL:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                s = str(IN).lower().strip()
                return event_value, s in ['true', '1']

            except Exception as e:
                logging.error("Error in F_STRING_AS_BOOL: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_STRING_AS_BOOL class destroyed')
