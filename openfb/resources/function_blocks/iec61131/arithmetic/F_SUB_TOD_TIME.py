import datetime
import re

_TIME_RE = re.compile(r'([-+]?\d+(?:\.\d+)?)(MS|D|H|M|S)', re.IGNORECASE)


def _parse_time(value):
    if isinstance(value, datetime.timedelta):
        return value
    if isinstance(value, bool):
        return datetime.timedelta(seconds=int(value))
    if isinstance(value, (int, float)):
        return datetime.timedelta(seconds=float(value))
    if isinstance(value, str):
        s = value.strip().upper()
        if s.startswith('T#'):
            s = s[2:]
        if not s:
            return None
        matches = _TIME_RE.findall(s)
        if matches:
            seconds = 0.0
            for num, unit in matches:
                n = float(num)
                u = unit.upper()
                if u == 'MS':
                    seconds += n / 1000.0
                elif u == 'S':
                    seconds += n
                elif u == 'M':
                    seconds += n * 60.0
                elif u == 'H':
                    seconds += n * 3600.0
                elif u == 'D':
                    seconds += n * 86400.0
            return datetime.timedelta(seconds=seconds)
        try:
            return datetime.timedelta(seconds=float(s))
        except ValueError:
            return None
    return None


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


def _apply_tod_delta(tod, delta):
    total = _tod_seconds(tod) + delta.total_seconds()
    total = total % 86400
    base = datetime.datetime(2000, 1, 1) + datetime.timedelta(seconds=total)
    return base.time()


class F_SUB_TOD_TIME:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            tod = _parse_tod(IN1)
            delta = _parse_time(IN2)
            if tod is None or delta is None:
                return None, None
            return event_value, _apply_tod_delta(tod, -delta)

    def __del__(self):
        print('F_SUB_TOD_TIME class destroyed')