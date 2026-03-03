import logging
from ...datetime_parsing import parse_datetime_value


class F_SUB_DT_DT:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            try:
                dt1 = parse_datetime_value(IN1)
                dt2 = parse_datetime_value(IN2)
                if dt1 is None or dt2 is None:
                    return event_value, None
                return event_value, dt1 - dt2

            except Exception as e:
                logging.error("Error in F_SUB_DT_DT: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_SUB_DT_DT class destroyed')