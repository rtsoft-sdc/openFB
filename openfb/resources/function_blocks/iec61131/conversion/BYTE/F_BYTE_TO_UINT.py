import logging
class F_BYTE_TO_UINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                val = int(IN) if not isinstance(IN, int) else IN
                return event_value, val & 0xFF

            except Exception as e:
                logging.error("Error in F_BYTE_TO_UINT: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_BYTE_TO_UINT class destroyed')
