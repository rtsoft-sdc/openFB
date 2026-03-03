import logging
class F_USINT_TO_WORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                return event_value, int(IN) & 0xFF

            except Exception as e:
                logging.error("Error in F_USINT_TO_WORD: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_USINT_TO_WORD class destroyed')
