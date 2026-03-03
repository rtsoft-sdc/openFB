import logging
from openfb.data_model_fboot.datetime_parser import parse_datetime_value, parse_time_interval


class F_SUB_DT_TIME:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            try:
                dt = parse_datetime_value(IN1)
                delta = parse_time_interval(IN2)
                if dt is None or delta is None:
                    return event_value, None
                return event_value, dt - delta

            except Exception as e:
                logging.error("Error in F_SUB_DT_TIME: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_SUB_DT_TIME class destroyed')