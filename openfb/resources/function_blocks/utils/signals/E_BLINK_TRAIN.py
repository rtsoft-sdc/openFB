import threading
import time


class E_BLINK_TRAIN:
    def __init__(self):
        self.timer_thread = None
        self.stop_flag = False
        self.timelow = 0
        self.timehigh = 0
        self.n_events = 0
        self.current_state = False
        self.event_callback = None
        
    def schedule(self, event_name, event_value, TIMELOW, TIMEHIGH, N):
        if event_name == 'START':
            self.stop_flag = False
            self.timelow = self._parse_time(TIMELOW)
            self.timehigh = self._parse_time(TIMEHIGH)
            self.n_events = int(N)
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
    
    def _parse_time(self, time_value):
        """Парсит TIME значение в секунды"""
        if isinstance(time_value, (int, float)):
            return time_value / 1000.0
        elif isinstance(time_value, str):
            time_str = time_value.upper().replace('T#', '').replace('MS', '').replace('S', '')
            try:
                return float(time_str) / 1000.0
            except:
                return 1.0
        return 1.0
    
    def _blink_loop(self):
        count = 0
        while not self.stop_flag and count < self.n_events:
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
            
            count += 1
        
        self.current_state = False
        if self.event_callback:
            self.event_callback('CNF', 1, self.current_state)
    
    def __del__(self):
        self.stop_flag = True
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join(timeout=1)
