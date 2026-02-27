import datetime


def _parse_tod(value):
    if isinstance(value, datetime.time):
        return value
    if isinstance(value, datetime.datetime):
        return value.time()
    if isinstance(value, str):
        s = value.strip()
        su = s.upper()
        if su.startswith('TOD#') or su.startswith('TIME_OF_DAY#'):
            s = s.split('#', 1)[1]
        try:
            return datetime.time.fromisoformat(s)
        except ValueError:
            try:
                return datetime.datetime.strptime(s, '%H:%M:%S').time()
            except ValueError:
                return None
    return None


def _tod_seconds(tod):
    return tod.hour * 3600 + tod.minute * 60 + tod.second + tod.microsecond / 1_000_000


class F_SUB_TOD_TOD:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            tod1 = _parse_tod(IN1)
            tod2 = _parse_tod(IN2)
            if tod1 is None or tod2 is None:
                return event_value, None
            diff = _tod_seconds(tod1) - _tod_seconds(tod2)
            return event_value, datetime.timedelta(seconds=diff)