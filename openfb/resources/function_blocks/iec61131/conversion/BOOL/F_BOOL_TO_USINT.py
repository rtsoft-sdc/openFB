import logging
class F_BOOL_TO_USINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                return event_value, 1 if IN else 0

            except Exception as e:
                logging.error("Error in F_BOOL_TO_USINT: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_BOOL_TO_USINT class destroyed')
