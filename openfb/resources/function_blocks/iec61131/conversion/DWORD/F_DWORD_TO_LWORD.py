import logging
class F_DWORD_TO_LWORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                val = int(IN) if not isinstance(IN, int) else IN
                return event_value, val & 0xFFFFFFFF

            except Exception as e:
                logging.error("Error in F_DWORD_TO_LWORD: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_DWORD_TO_LWORD class destroyed')
