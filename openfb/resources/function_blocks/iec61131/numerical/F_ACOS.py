import logging
import math

class F_ACOS:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                return event_value, math.acos(IN)

            except Exception as e:
                logging.error("Error in F_ACOS: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_ACOS class destroyed')