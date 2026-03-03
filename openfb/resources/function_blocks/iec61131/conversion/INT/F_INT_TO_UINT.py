import logging
class F_INT_TO_UINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                val = int(IN)
                return event_value, val if val >= 0 else val + 65536

            except Exception as e:
                logging.error("Error in F_INT_TO_UINT: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_INT_TO_UINT class destroyed')