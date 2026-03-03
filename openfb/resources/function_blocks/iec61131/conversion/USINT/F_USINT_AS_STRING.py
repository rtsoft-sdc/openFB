import logging
class F_USINT_AS_STRING:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                return event_value, str(int(IN) & 0xFF)

            except Exception as e:
                logging.error("Error in F_USINT_AS_STRING: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_USINT_AS_STRING class destroyed')
