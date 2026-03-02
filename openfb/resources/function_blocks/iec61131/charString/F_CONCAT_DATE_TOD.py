import datetime

class F_CONCAT_DATE_TOD:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            try:
                if hasattr(IN1, 'year') and hasattr(IN2, 'hour'):
                    return event_value, datetime.datetime.combine(IN1, IN2)
            except Exception:
                pass
            return event_value, ('' if IN1 is None else str(IN1)) + ' ' + ('' if IN2 is None else str(IN2))

    def __del__(self):
        print('F_CONCAT_DATE_TOD class destroyed')
