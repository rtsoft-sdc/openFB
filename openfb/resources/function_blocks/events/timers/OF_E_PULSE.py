import logging
import threading

class OF_E_PULSE:
    def __init__(self):
        self._timer = None
        self.Q = False

    def schedule(self, event_name, event_value, PT):
        """REQ -> set Q True and start PT to reset; R cancels and resets."""
        if event_name == 'REQ':
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

    def _set_false(self):
        self._timer = None
        self.Q = False

    def __del__(self):
        logging.info('E_PULSE class destroyed')
