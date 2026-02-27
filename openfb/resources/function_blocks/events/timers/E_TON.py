import threading

class E_TON:
    def __init__(self):
        self._timer = None
        self.Q = False

    def schedule(self, event_name, event_value, IN, PT):
        """On-delay: when IN=True start PT, on expiry set Q=True; if IN=False cancel and set Q=False."""
        if event_name == 'REQ':
            if IN:
                if self._timer:
                    self._timer.cancel()
                if PT and PT > 0:
                    self._timer = threading.Timer(PT, self._set_true)
                    self._timer.start()
                else:
                    self._set_true()
                    return event_value, self.Q
            else:
                if self._timer:
                    self._timer.cancel()
                    self._timer = None
                if self.Q:
                    self.Q = False
                    return event_value, self.Q
        return None

    def _set_true(self):
        self._timer = None
        self.Q = True