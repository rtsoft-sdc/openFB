class FB_R_TRIG:
    def __init__(self):
        self.mem = False 
    
    def schedule(self, event_name, event_value, CLK):
        if event_name == 'REQ':
            Q = CLK and (not self.mem)
            self.mem = CLK
            return event_value, Q