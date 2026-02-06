class F_DIV:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            if IN2 != 0:
                return event_value, IN1 / IN2