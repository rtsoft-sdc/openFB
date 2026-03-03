import logging
class F_SINT_TO_DWORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                val = int(IN)
                return event_value, val & 0xFF if val >= 0 else (val + 256) & 0xFFFFFFFF

            except Exception as e:
                logging.error("Error in F_SINT_TO_DWORD: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_SINT_TO_DWORD class destroyed')
