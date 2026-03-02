class F_INSERT:
    def schedule(self, event_name, event_value, IN1, IN2, P):
        if event_name == 'REQ':
            s = '' if IN1 is None else str(IN1)
            ins = '' if IN2 is None else str(IN2)
            try:
                p = int(P)
            except Exception:
                p = 0
            idx = max(0, p)
            if idx >= len(s):
                return event_value, s + ins
            return event_value, s[:idx] + ins + s[idx:]

    def __del__(self):
        print('F_INSERT class destroyed')
