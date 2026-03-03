import logging
class F_UINT_TO_REAL:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                return event_value, float(int(IN) & 0xFFFF)

            except Exception as e:
                logging.error("Error in F_UINT_TO_REAL: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_UINT_TO_REAL class destroyed')
