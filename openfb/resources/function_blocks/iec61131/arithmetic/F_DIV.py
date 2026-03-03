import logging
class F_DIV:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            try:
                if IN2 == 0:
                    return None, 0
                return event_value, IN1 / IN2
            except Exception:
                return None, 0

    def __del__(self):
        logging.info('F_DIV class destroyed')