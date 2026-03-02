class F_LEFT:
    def schedule(self, event_name, event_value, IN, L):
        if event_name == 'REQ':
            s = '' if IN is None else str(IN)
            try:
                n = int(L)
            except Exception:
                return None, ''
            if n <= 0:
                return None, ''
            return event_value, s[:n]

    def __del__(self):
        print('F_LEFT class destroyed')
