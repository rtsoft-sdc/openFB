import logging
class F_INT_TO_LINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                val = int(IN) if not isinstance(IN, int) else IN
                return event_value, val

            except Exception as e:
                logging.error("Error in F_INT_TO_LINT: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_INT_TO_LINT class destroyed')