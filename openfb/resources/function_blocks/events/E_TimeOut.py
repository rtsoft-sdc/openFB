import time
import threading
from datetime import timedelta

class E_TimeOut:
    """Timeout service - wraps E_DELAY through ATimeOut adapter interface"""
    def __init__(self):
        self._stop_event = threading.Event()
        self._timeout_thread = None
        self._on_timeout = None

    def set_timeout_callback(self, callback):
        self._on_timeout = callback

    def schedule(self, event_name, event_value, DT=None):
        if event_name == 'START':
            if DT is not None:
                self._stop_event.set()
                if self._timeout_thread and self._timeout_thread.is_alive():
                    self._timeout_thread.join(timeout=0.1)
                self._stop_event.clear()
                self._timeout_thread = threading.Thread(
                    target=self._wait_timeout,
                    args=(event_value, DT),
                    daemon=True
                )
                self._timeout_thread.start()
            return event_value
        elif event_name == 'STOP':
            self._stop_event.set()
            if self._timeout_thread and self._timeout_thread.is_alive():
                self._timeout_thread.join(timeout=0.1)
            return event_value

    def _wait_timeout(self, event_value, dt):
        if isinstance(dt, timedelta):
            delay = dt.total_seconds()
        else:
            delay = float(dt) / 1000.0 if isinstance(dt, (int, float)) else 0.001
        if not self._stop_event.wait(timeout=delay):
            if self._on_timeout:
                self._on_timeout(event_value)    
    def __del__(self):
        print('E_TimeOut class destroyed')
        if hasattr(self, '_stop_event'):
            self._stop_event.set()
        if hasattr(self, '_timeout_thread') and self._timeout_thread and self._timeout_thread.is_alive():
            self._timeout_thread.join(timeout=0.1)