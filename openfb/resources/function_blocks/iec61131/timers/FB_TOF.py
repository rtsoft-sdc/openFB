import logging
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


class FB_TOF:
    def __init__(self):
        self.start_time = None
        self.prev_in = False
        self.q = False
    
    def schedule(self, event_name, event_value, IN, PT):
        if event_name == 'REQ':
            try:
                now = time.monotonic()
                pt_delta = _parse_time(PT)
                PT_seconds = pt_delta.total_seconds()
                
                if IN and not self.prev_in:
                    self.q = True
                    self.start_time = None
                if not IN and self.prev_in:
                    self.start_time = now
                
                self.prev_in = IN
                
                if IN:
                    ET = timedelta(0)
                else:
                    if self.start_time is None:
                        ET = timedelta(0)
                    else:
                        elapsed_seconds = now - self.start_time
                        if elapsed_seconds < PT_seconds:
                            self.q = True
                            ET = timedelta(seconds=elapsed_seconds)
                        else:
                            self.q = False
                            ET = pt_delta
                
                return event_value, self.q, ET

            except Exception as e:
                logging.error("Error in FB_TOF: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('FB_TOF class destroyed')