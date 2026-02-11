class FB_TOF:
    def __init__(self):
        self.start_time = None
        self.q = False
    
    def schedule(self, event_name, event_value, IN, PT):
        if event_name == 'REQ':
            now = time.monotonic()
            
            if IN:
                self.q = True
                self.start_time = None
                ET = timedelta(0)
            else:
                if self.start_time is None:
                    self.start_time = now
                
                elapsed_seconds = now - self.start_time
                PT_seconds = PT.total_seconds()
                
                if elapsed_seconds < PT_seconds:
                    self.q = True
                    ET = timedelta(seconds=elapsed_seconds)
                else:
                    self.q = False
                    ET = PT
            
            return event_value, self.q, ET