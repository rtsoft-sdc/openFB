import time
from datetime import timedelta

class FB_TON:
    def __init__(self):
        self.start_time = None
        self.q = False
    
    def schedule(self, event_name, event_value, IN, PT):
        if event_name == 'REQ':
            now = time.monotonic()
            PT_seconds = PT.total_seconds()
            
            if IN:
                if self.start_time is None:
                    self.start_time = now
                
                elapsed = now - self.start_time
                ET = timedelta(seconds=min(elapsed, PT_seconds))
                
                self.q = elapsed >= PT_seconds
            else:
                self.start_time = None
                self.q = False
                ET = timedelta(0)
            
            return event_value, self.q, ET