import logging
import threading
import time
from datetime import timedelta

class E_RDELAY:
    """Reloadable delayed event propagation - cancellable"""
    def __init__(self):
        self._timer = None
        self._event_value = None
        self._on_timeout = None

    def set_on_timeout_callback(self, callback):
        self._on_timeout = callback

    def schedule(self, event_name, event_value, DT=None):
        if event_name == 'START':
            try:
                if DT is not None:
                    self._event_value = event_value
                    # Cancel any existing timer
                    if self._timer:
                        self._timer.cancel()
                    # Convert DT to seconds
                    if isinstance(DT, timedelta):
                        delay = DT.total_seconds()
                    else:
                        delay = float(DT) / 1000.0 if isinstance(DT, (int, float)) else 0.001
                    # Start new timer
                    self._timer = threading.Timer(delay, self._on_delay_complete)
                    self._timer.start()
                return event_value
            except Exception as e:
                logging.error("Error in E_RDELAY: %s", str(e))
                return None

        elif event_name == 'STOP':
            if self._timer:
                self._timer.cancel()
                self._timer = None
            return event_value
        return None

    def _on_delay_complete(self):
        if self._on_timeout:
            self._on_timeout(self._event_value)
        self._timer = None
    
    def __del__(self):
        logging.info('E_RDELAY class destroyed')
        if hasattr(self, '_timer') and self._timer:
            self._timer.cancel()