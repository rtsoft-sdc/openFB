from datetime import timedelta

class F_TIME_IN_S_TO_UDINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            td = IN if isinstance(IN, timedelta) else timedelta(milliseconds=int(IN))
            return event_value, int(td.total_seconds()) & 0xFFFFFFFF
