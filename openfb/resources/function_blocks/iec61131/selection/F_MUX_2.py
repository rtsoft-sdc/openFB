class F_MUX_2:
    def schedule(self, event_name, event_value, IN1, IN2, K):
        if event_name == 'REQ':
            return event_value, IN1 if K == 0 else IN2