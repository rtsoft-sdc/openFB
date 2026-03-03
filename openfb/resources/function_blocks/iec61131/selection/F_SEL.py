import logging
class F_SEL:
    def schedule(self, event_name, event_value, G, IN1, IN0):
        if event_name == 'REQ':
            try:
                return event_value, IN1 if G else IN0

            except Exception as e:
                logging.error("Error in F_SEL: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_SEL class destroyed')