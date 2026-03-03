import threading
import time
import logging
from ...datetime_parsing import parse_time_value_simple

class OF_E_BLINK:
    def __init__(self):
        self.timer_thread = None
        self.stop_flag = False
        self.timelow = 0
        self.timehigh = 0
        self.current_state = False
        self.event_callback = None
        
    def schedule(self, event_name, event_value, TIMELOW, TIMEHIGH):
        if event_name == 'START':
            self.stop_flag = False
            self.timelow = parse_time_value_simple(TIMELOW)
            self.timehigh = parse_time_value_simple(TIMEHIGH)
            self.current_state = False
            
            if self.timer_thread and self.timer_thread.is_alive():
                self.stop_flag = True
                self.timer_thread.join()
            
            self.timer_thread = threading.Thread(target=self._blink_loop, daemon=True)
            self.timer_thread.start()
            
            return event_value, self.current_state
            
        elif event_name == 'STOP':
            self.stop_flag = True
            if self.timer_thread and self.timer_thread.is_alive():
                self.timer_thread.join()
            self.current_state = False
            return event_value, self.current_state
            
        return event_value, self.current_state
    
    def _blink_loop(self):
        while not self.stop_flag:
            self.current_state = False
            if self.event_callback:
                self.event_callback('CNF', 1, self.current_state)
            time.sleep(self.timelow)
            
            if self.stop_flag:
                break
            
            self.current_state = True
            if self.event_callback:
                self.event_callback('CNF', 1, self.current_state)
            time.sleep(self.timehigh)
    
    def __del__(self):
        logging.info('OF_E_BLINK class destroyed')
        self.stop_flag = True
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join(timeout=1)
