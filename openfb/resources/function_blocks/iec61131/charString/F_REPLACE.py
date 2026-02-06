class F_REPLACE:
    def schedule(self, event_name, event_value, IN1, IN2, L, P):
        if event_name == 'REQ':
            s = '' if IN1 is None else str(IN1)
            rep = '' if IN2 is None else str(IN2)
            try:
                l = int(L)
            except Exception:
                l = 0
            try:
                p = int(P)
            except Exception:
                p = 1
            idx = max(0, p - 1)
            before = s[:idx]
            after = s[idx + max(0, l):]
            return event_value, before + rep + after
