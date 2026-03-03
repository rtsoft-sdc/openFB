import logging
class F_ULINT_TO_INT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                val = int(IN) & 0xFFFF
                return event_value, val if val < 32768 else val - 65536

            except Exception as e:
                logging.error("Error in F_ULINT_TO_INT: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_ULINT_TO_INT class destroyed')
