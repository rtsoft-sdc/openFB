import logging
from datetime import timedelta

class F_TIME_IN_MS_TO_ULINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                td = IN if isinstance(IN, timedelta) else timedelta(milliseconds=int(IN))
                return event_value, int(td.total_seconds() * 1000) & 0xFFFFFFFFFFFFFFFF

            except Exception as e:
                logging.error("Error in F_TIME_IN_MS_TO_ULINT: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_TIME_IN_MS_TO_ULINT class destroyed')
