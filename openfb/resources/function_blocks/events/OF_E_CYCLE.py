import logging
import time
import threading
from openfb.data_model_fboot.datetime_parser import parse_time_value_simple

class OF_E_CYCLE:

    def __init__(self):
        self._stop_event = threading.Event()
        self._cycle_thread = None
        self._on_event = None
        self._event_value = None
        self._event_counter = 0
    
    def set_on_event_callback(self, callback):
        self._on_event = callback

    def schedule(self, event_name, event_value, DT):
        if event_name == 'START':
            try:
                self._stop_event.set()
                if self._cycle_thread and self._cycle_thread.is_alive():
                    self._cycle_thread.join(timeout=0.5)
                
                self._event_value = event_value
                self._event_counter = event_value  
                
                delay_seconds = parse_time_value_simple(DT)

                self._stop_event.clear()
                self._cycle_thread = threading.Thread(
                    target=self._cycle_loop,
                    args=(delay_seconds,),
                    daemon=True
                )
                self._cycle_thread.start()
                
                return (event_value,)
            
            except Exception as e:
                logging.error("Error in OF_E_CYCLE: %s", str(e))
                return (None,)

        elif event_name == 'STOP':
            self._stop_event.set()
            if self._cycle_thread and self._cycle_thread.is_alive():
                self._cycle_thread.join(timeout=0.5)
            return (None,)
        
    def _cycle_loop(self, delay_seconds):
        while not self._stop_event.is_set():
            if self._stop_event.wait(timeout=delay_seconds):
                break
            
            if not self._stop_event.is_set():
                self._event_counter += 1
                if self._on_event:
                    self._on_event('EO', self._event_value) # временно так 
    
    def __del__(self):
        if hasattr(self, '_stop_event'):
            self._stop_event.set()
        if hasattr(self, '_cycle_thread') and self._cycle_thread and self._cycle_thread.is_alive():
            self._cycle_thread.join(timeout=0.5)
