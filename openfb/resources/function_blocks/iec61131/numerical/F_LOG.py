import logging
import math

class F_LOG:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                return event_value, math.log10(IN)

            except Exception as e:
                logging.error("Error in F_LOG: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_LOG class destroyed')
