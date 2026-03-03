import logging
import math

class F_COS:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                return event_value, math.cos(IN)

            except Exception as e:
                logging.error("Error in F_COS: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_COS class destroyed')