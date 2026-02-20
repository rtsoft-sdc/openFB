import threading

class E_TONOF:
    def __init__(self):
        self._timer_on = None
        self._timer_off = None
        self.Q = False

    def schedule(self, event_name, event_value, IN, PT_ON, PT_OFF):
        """On/off delay: when IN True -> start PT_ON to set Q True; when IN False -> start PT_OFF to set Q False."""
        if event_name == 'REQ':
            if IN:
                if self._timer_off:
                    self._timer_off.cancel()
                    self._timer_off = None
                if self._timer_on:
                    self._timer_on.cancel()
                if PT_ON and PT_ON > 0:
                    self._timer_on = threading.Timer(PT_ON, self._set_true)
                    self._timer_on.start()
                else:
                    self._set_true()
                    return event_value, self.Q
            else:
                if self._timer_on:
                    self._timer_on.cancel()
                    self._timer_on = None
                if self._timer_off:
                    self._timer_off.cancel()
                if PT_OFF and PT_OFF > 0:
                    self._timer_off = threading.Timer(PT_OFF, self._set_false)
                    self._timer_off.start()
                else:
                    self._set_false()
                    return event_value, self.Q
        elif event_name == 'R':
            if self._timer_on:
                self._timer_on.cancel()
                self._timer_on = None
            if self._timer_off:
                self._timer_off.cancel()
                self._timer_off = None
            if self.Q:
                self.Q = False
                return event_value, self.Q
        return None

    def _set_true(self):
        self._timer_on = None
        self.Q = True

    def _set_false(self):
        self._timer_off = None
        self.Q = False

# import asyncio
# class E_TONOFAsync(E_TONOF):
#     async def schedule(self, event_name, event_value, IN=None, PT_ON=None, PT_OFF=None, callback=None):
#         if event_name == 'REQ':
#             if IN:
#                 await asyncio.sleep(PT_ON)
#                 self.Q = True
#                 if callback: callback(event_value, self.Q)
#             else:
#                 await asyncio.sleep(PT_OFF)
#                 self.Q = False
#                 if callback: callback(event_value, self.Q)