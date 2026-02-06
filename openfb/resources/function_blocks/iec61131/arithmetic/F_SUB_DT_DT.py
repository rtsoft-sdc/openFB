class F_SUB_DT_DT:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            return event_value, IN1 - IN2