class F_SHL:
    def schedule(self, event_name, event_value, IN, N):
        if event_name == 'REQ':
            try:
                return event_value, int(IN) << int(N)
            except Exception:
                return event_value, 0
