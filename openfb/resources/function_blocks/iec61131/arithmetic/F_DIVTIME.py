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
            td = _parse_time(IN1)
            n = _parse_number(IN2)
            if td is None or n in (None, 0):
                return None, datetime.timedelta(0)
            return event_value, datetime.timedelta(seconds=td.total_seconds() / n)

    def __del__(self):
        print('F_DIVTIME class destroyed')