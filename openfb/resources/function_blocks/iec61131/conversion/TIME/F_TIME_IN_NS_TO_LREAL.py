from datetime import timedelta

class F_TIME_IN_NS_TO_LREAL:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            td = IN if isinstance(IN, timedelta) else timedelta(milliseconds=int(IN))
            return event_value, float(td.total_seconds() * 1000000000)

    def __del__(self):
        print('F_TIME_IN_NS_TO_LREAL class destroyed')
