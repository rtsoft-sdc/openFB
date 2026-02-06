class AND_6:
    def schedule(self, event_name, event_value, IN1, IN2, IN3, IN4, IN5, IN6):
        if event_name == 'REQ':
            try:
                return event_value, int(IN1) & int(IN2) & int(IN3) & int(IN4) & int(IN5) & int(IN6)
            except Exception:
                return event_value, 0
