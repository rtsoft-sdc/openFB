import logging
import threading
from datetime import timedelta
from openfb.data_model_fboot.datetime_parser import parse_time_value_simple

class E_DELAY:
    
    def __init__(self):
        self._stop_event = threading.Event()
        self._delay_thread = None
        self._on_event = None
        self._event_value = None
        self._event_counter = 0
    
    def set_on_event_callback(self, callback):
        self._on_event = callback
    
    def schedule(self, event_name, event_value, DT):
        if event_name == 'START':
            try:
                if self._delay_thread and self._delay_thread.is_alive():
                    return (None,)
                
                self._event_counter = event_value if self._event_counter == 0 else self._event_counter + 1
                self._event_value = self._event_counter
                
                delay_seconds = parse_time_value_simple(DT)

                self._stop_event.clear()
                self._delay_thread = threading.Thread(
                    target=self._delay_loop,
                    args=(delay_seconds,),
                    daemon=True
                )
                self._delay_thread.start()
                return (event_value,)
            
            except Exception as e:
                logging.error("Error in E_DELAY: %s", str(e))
                return (None,)

        elif event_name == 'STOP':
            self._stop_event.set()
            if self._delay_thread and self._delay_thread.is_alive():
                self._delay_thread.join(timeout=0.5)
            return (None,)
        
        return (None,)
    
    def _delay_loop(self, delay_seconds):
        if not self._stop_event.wait(timeout=delay_seconds):
            if self._on_event:
                self._on_event('EO', self._event_value)
    
    def __del__(self):
        logging.info('E_DELAY class destroyed')
        if hasattr(self, '_stop_event'):
            self._stop_event.set()
        if hasattr(self, '_delay_thread') and self._delay_thread and self._delay_thread.is_alive():
            self._delay_thread.join(timeout=0.5)