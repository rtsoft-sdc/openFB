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


def _parse_dt(value):
    if isinstance(value, datetime.datetime):
        return value
    if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
        return datetime.datetime.combine(value, datetime.time())
    if isinstance(value, str):
        s = value.strip()
        su = s.upper()
        if su.startswith('DT#') or su.startswith('DATE_AND_TIME#'):
            s = s.split('#', 1)[1]
        for fmt in ('%Y-%m-%d-%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S'):
            try:
                return datetime.datetime.strptime(s, fmt)
            except ValueError:
                pass
        try:
            return datetime.datetime.fromisoformat(s)
        except ValueError:
            pass
        try:
            d = datetime.date.fromisoformat(s)
            return datetime.datetime.combine(d, datetime.time())
        except ValueError:
            return None
    return None


class F_ADD_DT_TIME:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            dt = _parse_dt(IN1)
            delta = _parse_time(IN2)
            if dt is None or delta is None:
                return None, None
            return event_value, dt + delta

    def __del__(self):
        print('F_ADD_DT_TIME class destroyed')