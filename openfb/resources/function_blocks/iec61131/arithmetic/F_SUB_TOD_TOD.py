import logging
import datetime
from .datetime_parsing import parse_time_of_day, tod_seconds


class F_SUB_TOD_TOD:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            try:
                tod1 = parse_time_of_day(IN1)
                tod2 = parse_time_of_day(IN2)
                if tod1 is None or tod2 is None:
                    return event_value, None
                diff = tod_seconds(tod1) - tod_seconds(tod2)
                return event_value, datetime.timedelta(seconds=diff)

            except Exception as e:
                logging.error("Error in F_SUB_TOD_TOD: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_SUB_TOD_TOD class destroyed')