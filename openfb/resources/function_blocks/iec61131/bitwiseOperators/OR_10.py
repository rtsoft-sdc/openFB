class OR_10:
    def schedule(self, event_name, event_value, IN1, IN2, IN3, IN4, IN5, IN6, IN7, IN8, IN9, IN10):
        if event_name == 'REQ':
            try:
                vals = (IN1,IN2,IN3,IN4,IN5,IN6,IN7,IN8,IN9,IN10)
                res = int(vals[0])
                for v in vals[1:]:
                    res |= int(v)
                return event_value, res
            except Exception:
                return event_value, 0
