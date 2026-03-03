import logging
class F_LWORD_TO_LINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                val = int(IN) & 0xFFFFFFFFFFFFFFFF
                return event_value, val if val < 0x8000000000000000 else val - 0x10000000000000000

            except Exception as e:
                logging.error("Error in F_LWORD_TO_LINT: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_LWORD_TO_LINT class destroyed')
