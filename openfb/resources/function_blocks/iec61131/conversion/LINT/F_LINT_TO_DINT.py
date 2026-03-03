import logging
class F_LINT_TO_DINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                val = int(IN) & 0xFFFFFFFF
                return event_value, val if val < 0x80000000 else val - 0x100000000

            except Exception as e:
                logging.error("Error in F_LINT_TO_DINT: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_LINT_TO_DINT class destroyed')
