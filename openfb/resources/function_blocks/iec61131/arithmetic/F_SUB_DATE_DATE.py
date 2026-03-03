import logging
from .datetime_parsing import parse_date_value


class F_SUB_DATE_DATE:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            try:
                d1 = parse_date_value(IN1)
                d2 = parse_date_value(IN2)
                if d1 is None or d2 is None:
                    return event_value, None
                return event_value, d1 - d2

            except Exception as e:
                logging.error("Error in F_SUB_DATE_DATE: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_SUB_DATE_DATE class destroyed')