class F_LEN:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            if IN is None:
                return event_value, 0
            try:
                return event_value, len(IN)
            except Exception:
                return event_value, 0
