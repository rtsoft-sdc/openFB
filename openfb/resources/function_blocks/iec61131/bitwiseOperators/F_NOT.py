class F_NOT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                return event_value, ~int(IN)
            except Exception:
                return event_value, 0
