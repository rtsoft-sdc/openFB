class F_CONCAT:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            a = '' if IN1 is None else str(IN1)
            b = '' if IN2 is None else str(IN2)
            return event_value, a + b
