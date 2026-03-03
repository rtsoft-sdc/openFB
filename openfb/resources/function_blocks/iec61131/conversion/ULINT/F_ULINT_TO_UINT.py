import logging
class F_ULINT_TO_UINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                return event_value, int(IN) & 0xFFFF

            except Exception as e:
                logging.error("Error in F_ULINT_TO_UINT: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_ULINT_TO_UINT class destroyed')
