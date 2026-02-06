class ADD_3:
    def schedule(self, event_name, event_value, IN1, IN2, IN3):
        if event_name == 'REQ':
            return event_value, IN1 + IN2 + IN3