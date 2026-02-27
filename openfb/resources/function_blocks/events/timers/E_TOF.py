import threading

class E_TOF:
    def __init__(self):
        self._timer = None
        self.Q = False

    def schedule(self, event_name, event_value, IN, PT):
        """Off-delay: when IN=True set Q=True immediately; when IN=False start PT to set Q=False."""
        if event_name == 'REQ':
            if IN:
                if self._timer:
                    self._timer.cancel()
                    self._timer = None
                if not self.Q:
                    self.Q = True
                    return event_value, self.Q
            else:
                if self._timer:
                    self._timer.cancel()
                if PT and PT > 0:
                    self._timer = threading.Timer(PT, self._set_false)
                    self._timer.start()
                else:
                    if self.Q:
                        self.Q = False
                        return event_value, self.Q
        elif event_name == 'R':
            if self._timer:
                self._timer.cancel()
                self._timer = None
            if self.Q:
                self.Q = False
                return event_value, self.Q
        return None

    def _set_false(self):
        self._timer = None
        self.Q = False