import logging
class F_INT_TO_DWORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                val = int(IN) if not isinstance(IN, int) else IN
                return event_value, val & 0xFFFF if val >= 0 else (val + 65536) & 0xFFFFFFFF

            except Exception as e:
                logging.error("Error in F_INT_TO_DWORD: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_INT_TO_DWORD class destroyed')