import logging
class F_STRING_AS_LWORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                return event_value, int(str(IN)) & 0xFFFFFFFFFFFFFFFF

            except Exception as e:
                logging.error("Error in F_STRING_AS_LWORD: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_STRING_AS_LWORD class destroyed')
