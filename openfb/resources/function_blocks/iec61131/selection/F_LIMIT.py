class F_LIMIT:
    def schedule(self, event_name, event_value, MN, IN, MX):
        if event_name == 'REQ':
            return event_value, max(MN, min(IN, MX))