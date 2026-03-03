import datetime
import re


_TIME_RE = re.compile(r'([-+]?\d+(?:\.\d+)?)(MS|D|H|M|S)', re.IGNORECASE)


def parse_time_interval(value):
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


def parse_datetime_value(value):
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


def parse_date_value(value):
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


def parse_time_of_day(value):
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


def tod_seconds(tod):
    return tod.hour * 3600 + tod.minute * 60 + tod.second + tod.microsecond / 1_000_000


def apply_tod_delta(tod, delta):
    total = tod_seconds(tod) + delta.total_seconds()
    total = total % 86400
    base = datetime.datetime(2000, 1, 1) + datetime.timedelta(seconds=total)
    return base.time()


def parse_time_value_simple(time_value):
    if isinstance(time_value, datetime.timedelta):
        return time_value.total_seconds()
    if isinstance(time_value, (int, float)):
        return time_value / 1000.0 if time_value > 100 else time_value
    if isinstance(time_value, str):
        s = time_value.upper().strip()
        if s.startswith('T#'):
            s = s[2:]
        
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
            return seconds
        
        try:
            val = float(s)
            return val / 1000.0 if val > 100 else val
        except ValueError:
            return 1.0
    
    return 1.0



def parse_number(value):
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
