import logging
class F_REAL_TO_SINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                return event_value, int(float(IN))

            except Exception as e:
                logging.error("Error in F_REAL_TO_SINT: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_REAL_TO_SINT class destroyed')
