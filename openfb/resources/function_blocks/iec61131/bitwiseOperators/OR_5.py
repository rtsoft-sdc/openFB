class OR_5:
    def schedule(self, event_name, event_value, IN1, IN2, IN3, IN4, IN5):
        if event_name == 'REQ':
            res = int(IN1)
            for v in (IN2, IN3, IN4, IN5):
                res |= int(v)
            return event_value, res

    def __del__(self):
        print('OR_5 class destroyed')
