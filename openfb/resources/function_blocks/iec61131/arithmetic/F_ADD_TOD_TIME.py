import logging
from ...datetime_parsing import parse_time_of_day, parse_time_interval, apply_tod_delta


class F_ADD_TOD_TIME:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            try:
                tod = parse_time_of_day(IN1)
                delta = parse_time_interval(IN2)
                if tod is None or delta is None:
                    return event_value, None
                return event_value, apply_tod_delta(tod, delta)
            
            except Exception as e:
                logging.error("Error in F_ADD_TOD_TIME: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_ADD_TOD_TIME class destroyed')