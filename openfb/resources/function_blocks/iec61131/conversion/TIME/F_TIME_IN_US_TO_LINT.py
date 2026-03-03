import logging
from datetime import timedelta

class F_TIME_IN_US_TO_LINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                td = IN if isinstance(IN, timedelta) else timedelta(milliseconds=int(IN))
                return event_value, int(td.total_seconds() * 1000000)

            except Exception as e:
                logging.error("Error in F_TIME_IN_US_TO_LINT: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_TIME_IN_US_TO_LINT class destroyed')
