import time
import threading

class E_CYCLE:

    def __init__(self):
        self._stop_event = threading.Event()
        self._cycle_thread = None
        self._fb_interface = None 
        self._event_value = None
    
    def set_fb_interface(self, fb_interface):
        self._fb_interface = fb_interface
    
    def schedule(self, event_name, event_value, DT):
        if event_name == 'START':
            self._stop_event.set()
            if self._cycle_thread and self._cycle_thread.is_alive():
                self._cycle_thread.join(timeout=0.1)
            
            self._event_value = event_value
            
            delay_seconds = DT / 1000.0 if isinstance(DT, (int, float)) and DT > 0 else 0.001

            self._stop_event.clear()
            self._cycle_thread = threading.Thread(
                target=self._cycle_loop,
                args=(delay_seconds,),
                daemon=True
            )
            self._cycle_thread.start()
            
            return event_value
            
        elif event_name == 'STOP':
            self._stop_event.set()
            return None
            
        return None
    
    def _cycle_loop(self, delay_seconds):
        while not self._stop_event.is_set():
            time.sleep(delay_seconds)
            
            if not self._stop_event.is_set() and self._fb_interface:
                self._fb_interface.push_event('EO', self._event_value)
    
    def __del__(self):
        print('E_CYCLE class destroyed')
        if hasattr(self, '_stop_event'):
            self._stop_event.set()
        if hasattr(self, '_cycle_thread') and self._cycle_thread and self._cycle_thread.is_alive():
            self._cycle_thread.join(timeout=0.1)
