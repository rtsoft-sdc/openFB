class F_SEL:
    def schedule(self, event_name, event_value, G, IN1, IN0):
        if event_name == 'REQ':
            return event_value, IN1 if G else IN0