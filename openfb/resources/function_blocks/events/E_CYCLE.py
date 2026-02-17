import time
import logging 

class E_CYCLE:
    def __init__(self):
        self.running = False
        self.period = 0.0
        self.next_trigger = 0.0
    
    def _parse_time(self, dt_value):
        if hasattr(dt_value, 'total_seconds'):  # timedelta
            return dt_value.total_seconds()
        elif isinstance(dt_value, (int, float)):
            return float(dt_value)
        elif isinstance(dt_value, str):
            s = dt_value.strip().upper()
            if s.startswith('T#'):
                s = s[2:]
            if s.endswith('MS'):
                return float(s[:-2].strip()) / 1000.0
            s = s.rstrip('S')
            return float(s)
        
    def schedule(self, event_name, event_value, DT=None):
        now = time.monotonic()
    
        if self.running and now >= self.next_trigger:
            self.next_trigger += self.period
            if now > self.next_trigger:
                self.next_trigger = now + self.period
            return 'EO'
        
        if event_name == 'START':
            if DT is None:
                logging.error("Параметр DT обязателен для события START")
            
            self.period = self._parse_time(DT)
            if self.period <= 0:
                logging.error(f"Период должен быть положительным: {self.period}")
            
            self.next_trigger = now + self.period
            self.running = True
            return None
        
        elif event_name == 'STOP':
            self.running = False
            return None
        
        return None