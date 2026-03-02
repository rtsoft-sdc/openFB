import time
from datetime import timedelta
import re

_TIME_RE = re.compile(r'([-+]?\d+(?:\.\d+)?)(MS|D|H|M|S)', re.IGNORECASE)


def _parse_time(value):
    if isinstance(value, timedelta):
        return value
    if isinstance(value, (int, float)):
        return timedelta(seconds=float(value))
    if isinstance(value, str):
        s = value.strip().upper()
        if s.startswith('T#'):
            s = s[2:]
        if not s:
            return timedelta(0)
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
            return timedelta(seconds=seconds)
        try:
            return timedelta(seconds=float(s))
        except ValueError:
            return timedelta(0)
    return timedelta(0)


class FB_TP:
    def __init__(self):
        self.start_time = None
        self.prev_in = False
        self.q = False
        self.pulse_active = False
    
    def schedule(self, event_name, event_value, IN, PT):
        if event_name == 'REQ':
            now = time.monotonic()
            pt_delta = _parse_time(PT)
            PT_seconds = pt_delta.total_seconds()
            
            if not self.prev_in and IN and not self.pulse_active:
                self.start_time = now
                self.pulse_active = True
                self.q = True
            
            self.prev_in = IN
            
            if self.pulse_active and self.start_time is not None:
                elapsed = now - self.start_time
                if elapsed < PT_seconds:
                    self.q = True
                    ET = timedelta(seconds=elapsed)
                else:
                    self.q = False
                    self.pulse_active = False
                    ET = pt_delta
            else:
                self.q = False
                ET = timedelta(0)
            
            return event_value, self.q, ET

    def __del__(self):
        print('FB_TP class destroyed')