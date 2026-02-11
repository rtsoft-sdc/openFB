import time
from datetime import timedelta

class FB_TP:
    def __init__(self):
        self.start_time = None
        self.prev_in = False
        self.q = False
    
    def schedule(self, event_name, event_value, IN, PT):
        if event_name == 'REQ':
            now = time.monotonic()
            PT_seconds = PT.total_seconds()
            
            if not self.prev_in and IN:
                self.start_time = now
            
            self.prev_in = IN
            
            if self.start_time is not None:
                elapsed = now - self.start_time
                ET = timedelta(seconds=min(elapsed, PT_seconds))
                self.q = elapsed < PT_seconds
                
                if not self.q:
                    self.start_time = None
            else:
                self.q = False
                ET = timedelta(0)
            
            return event_value, self.q, ET