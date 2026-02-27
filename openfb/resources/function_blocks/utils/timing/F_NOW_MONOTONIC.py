import time

class F_NOW_MONOTONIC:
    def schedule(self, event_name, event_value):
        if event_name == 'REQ':
            monotonic_time = int(time.monotonic() * 1000)
            return event_value, monotonic_time
        return event_value, None
