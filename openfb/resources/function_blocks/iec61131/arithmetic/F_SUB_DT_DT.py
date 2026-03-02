import datetime


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


class F_SUB_DT_DT:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            dt1 = _parse_dt(IN1)
            dt2 = _parse_dt(IN2)
            if dt1 is None or dt2 is None:
                return None, None
            return event_value, dt1 - dt2

    def __del__(self):
        print('F_SUB_DT_DT class destroyed')