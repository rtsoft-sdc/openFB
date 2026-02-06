class F_LEFT:
    def schedule(self, event_name, event_value, IN, L):
        if event_name == 'REQ':
            s = '' if IN is None else str(IN)
            try:
                n = int(L)
            except Exception:
                return event_value, ''
            if n <= 0:
                return event_value, ''
            return event_value, s[:n]
