class XOR_4:
    def schedule(self, event_name, event_value, IN1, IN2, IN3, IN4):
        if event_name == 'REQ':
            try:
                return event_value, int(IN1) ^ int(IN2) ^ int(IN3) ^ int(IN4)
            except Exception:
                return event_value, 0
