import logging
class F_ULINT_TO_LREAL:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                return event_value, float(int(IN) & 0xFFFFFFFFFFFFFFFF)

            except Exception as e:
                logging.error("Error in F_ULINT_TO_LREAL: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_ULINT_TO_LREAL class destroyed')
