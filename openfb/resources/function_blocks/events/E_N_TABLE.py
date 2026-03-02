import time
import threading
from datetime import timedelta

class E_N_TABLE:
    """Generation of a finite train of separate events using E_TABLE + E_DEMUX"""
    def __init__(self):
        self._stop_event = threading.Event()
        self._thread = None
        self._DT = []
        self._N = 0
        self._on_event = None

    def set_on_event_callback(self, callback):
        self._on_event = callback

    def schedule(self, event_name, event_value, DT=None, N=None):
        if event_name == 'START':
            if DT is not None and N is not None:
                self._DT = DT if isinstance(DT, (list, tuple)) else [DT]
                self._N = N
                self._stop_event.set()
                if self._thread and self._thread.is_alive():
                    self._thread.join(timeout=0.5)
                self._stop_event.clear()
                self._thread = threading.Thread(
                    target=self._generate_events,
                    args=(event_value,),
                    daemon=True
                )
                self._thread.start()
            return event_value
        elif event_name == 'STOP':
            self._stop_event.set()
            if self._thread and self._thread.is_alive():
                self._thread.join(timeout=0.5)
            return event_value
        return None

    def _generate_events(self, event_value):
        """Generate N events with delays from DT array, demuxed to EO0-EO3"""
        for i in range(min(self._N, 4)):  # E_N_TABLE has 4 outputs (EO0-EO3)
            if self._stop_event.is_set():
                break
            # Generate demuxed event output
            output_name = f'EO{i}'
            if self._on_event:
                self._on_event(output_name, event_value, i)
            # Wait for next event delay
            if i < len(self._DT) - 1:
                dt_val = self._DT[i]
                if isinstance(dt_val, timedelta):
                    delay = dt_val.total_seconds()
                else:
                    delay = float(dt_val) / 1000.0 if isinstance(dt_val, (int, float)) else 0.001
                if not self._stop_event.wait(timeout=delay):
                    continue
                else:
                    break
    
    def __del__(self):
        print('E_N_TABLE class destroyed')
        if hasattr(self, '_stop_event'):
            self._stop_event.set()
        if hasattr(self, '_thread') and self._thread and self._thread.is_alive():
            self._thread.join(timeout=0.5)