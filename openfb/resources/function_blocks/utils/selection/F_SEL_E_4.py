class F_SEL_E_4:
    def schedule(self, event_name, event_value, IN1, IN2, IN3, IN4):
        if event_name == 'REQ1':
            return event_value, IN1
        elif event_name == 'REQ2':
            return event_value, IN2
        elif event_name == 'REQ3':
            return event_value, IN3
        elif event_name == 'REQ4':
            return event_value, IN4
