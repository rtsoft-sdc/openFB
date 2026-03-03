import logging
class F_MUX_2:
    def schedule(self, event_name, event_value, IN1, IN2, K):
        if event_name == 'REQ':
            try:
                return event_value, IN1 if K == 0 else IN2

            except Exception as e:
                logging.error("Error in F_MUX_2: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_MUX_2 class destroyed')