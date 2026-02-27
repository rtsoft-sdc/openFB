import datetime


def _parse_date(value):
    if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
        return value
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, str):
        s = value.strip()
        su = s.upper()
        if su.startswith('D#') or su.startswith('DATE#'):
            s = s.split('#', 1)[1]
        try:
            return datetime.date.fromisoformat(s)
        except ValueError:
            return None
    return None


class F_SUB_DATE_DATE:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            d1 = _parse_date(IN1)
            d2 = _parse_date(IN2)
            if d1 is None or d2 is None:
                return event_value, None
            return event_value, d1 - d2