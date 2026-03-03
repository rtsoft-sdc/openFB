import logging
import datetime
from ...datetime_parsing import parse_time_interval, parse_number



class F_MULTIME:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            try:
                td = parse_time_interval(IN1)
                n = parse_number(IN2)
                if td is None or n is None:
                    return event_value, datetime.timedelta(0)
                return event_value, datetime.timedelta(seconds=td.total_seconds() * n)

            except Exception as e:
                logging.error("Error in F_MULTIME: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_MULTIME class destroyed')