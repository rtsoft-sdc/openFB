class F_SEL_E_2:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ1':
            return event_value, IN1
        elif event_name == 'REQ2':
            return event_value, IN2
