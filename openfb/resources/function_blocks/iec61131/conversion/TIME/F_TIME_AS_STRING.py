import logging
import re
from datetime import timedelta

class F_TIME_AS_STRING:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                td = IN if isinstance(IN, timedelta) else timedelta(milliseconds=int(IN))
                total_ms = int(td.total_seconds() * 1000)
                return event_value, f"T#{total_ms}MS"

            except Exception as e:
                logging.error("Error in F_TIME_AS_STRING: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_TIME_AS_STRING class destroyed')
