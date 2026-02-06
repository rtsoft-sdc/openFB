class F_DELETE:
    def schedule(self, event_name, event_value, IN, L, P):
        if event_name == 'REQ':
            s = '' if IN is None else str(IN)
            try:
                l = int(L)
            except Exception:
                l = 0
            try:
                p = int(P)
            except Exception:
                p = 1
            start = max(0, p - 1)
            if l <= 0:
                return event_value, s
            return event_value, s[:start] + s[start + l:]
