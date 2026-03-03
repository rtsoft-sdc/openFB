import logging
class F_WSTRING_TO_STRING:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                return event_value, str(IN)

            except Exception as e:
                logging.error("Error in F_WSTRING_TO_STRING: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_WSTRING_TO_STRING class destroyed')
