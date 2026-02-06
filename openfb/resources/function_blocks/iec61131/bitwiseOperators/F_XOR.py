class F_XOR:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            try:
                return event_value, int(IN1) ^ int(IN2)
            except Exception:
                return event_value, 0
