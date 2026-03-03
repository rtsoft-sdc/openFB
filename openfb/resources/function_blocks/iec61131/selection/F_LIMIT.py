import logging
class F_LIMIT:
    def schedule(self, event_name, event_value, MN, IN, MX):
        if event_name == 'REQ':
            try:
                return event_value, max(MN, min(IN, MX))

            except Exception as e:
                logging.error("Error in F_LIMIT: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_LIMIT class destroyed')