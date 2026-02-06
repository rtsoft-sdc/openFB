import datetime

class F_SUB_TOD_TOD:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            dt1 = datetime.datetime.combine(datetime.date.min, IN1)
            dt2 = datetime.datetime.combine(datetime.date.min, IN2)
            return event_value, dt1 - dt2