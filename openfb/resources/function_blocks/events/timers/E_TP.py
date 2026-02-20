import threading

class E_TP:
    def __init__(self):
        self._timer = None
        self.Q = False

    def schedule(self, event_name, event_value, IN, PT):
        """Pulse: on REQ with IN True -> set Q True and start PT to reset; R resets immediately."""
        if event_name == 'REQ':
            if IN:
                if self._timer:
                    self._timer.cancel()
                self.Q = True
                if PT and PT > 0:
                    self._timer = threading.Timer(PT, self._set_false)
                    self._timer.start()
                else:
                    self._set_false()
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

# import asyncio
# class E_TPAsync(E_TP):
#     async def schedule(self, event_name, event_value, IN=None, PT=None, callback=None):
#         if event_name == 'REQ' and IN:
#             self.Q = True
#             if callback: callback(event_value, self.Q)
#             await asyncio.sleep(PT)
#             self.Q = False
#             if callback: callback(event_value, self.Q)