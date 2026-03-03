import logging
import datetime
from openfb.data_model_fboot.datetime_parser import parse_time_interval


def _parse_number(value):
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return None
    return None


class F_DIVTIME:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            try:
                td = parse_time_interval(IN1)
                n = _parse_number(IN2)
                if td is None or n in (None, 0):
                    return event_value, datetime.timedelta(0)
                return event_value, datetime.timedelta(seconds=td.total_seconds() / n)

            except Exception as e:
                logging.error("Error in F_DIVTIME: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_DIVTIME class destroyed')