import logging
class F_LINT_TO_SINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                val = int(IN) & 0xFF
                return event_value, val if val < 128 else val - 256

            except Exception as e:
                logging.error("Error in F_LINT_TO_SINT: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_LINT_TO_SINT class destroyed')
