import logging
class F_LWORD_TO_DWORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                return event_value, int(IN) & 0xFFFFFFFF

            except Exception as e:
                logging.error("Error in F_LWORD_TO_DWORD: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_LWORD_TO_DWORD class destroyed')
