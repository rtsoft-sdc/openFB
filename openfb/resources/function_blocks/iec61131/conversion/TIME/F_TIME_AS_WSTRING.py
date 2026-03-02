import re
from datetime import timedelta

class F_TIME_AS_WSTRING:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            td = IN if isinstance(IN, timedelta) else timedelta(milliseconds=int(IN))
            total_ms = int(td.total_seconds() * 1000)
            return event_value, f"T#{total_ms}MS"

    def __del__(self):
        print('F_TIME_AS_WSTRING class destroyed')
