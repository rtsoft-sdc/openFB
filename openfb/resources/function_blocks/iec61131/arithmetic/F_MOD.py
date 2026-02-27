class F_MOD:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            try:
                if IN2 == 0:
                    return event_value, 0
                return event_value, IN1 % IN2
            except Exception:
                return event_value, 0