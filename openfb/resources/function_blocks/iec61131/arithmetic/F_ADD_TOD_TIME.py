import datetime

class F_ADD_TOD_TIME:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            dt = datetime.datetime.combine(datetime.date.min, IN1) + IN2
            return event_value, dt.time()