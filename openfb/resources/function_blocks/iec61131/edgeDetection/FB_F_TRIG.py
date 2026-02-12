class FB_F_TRIG:
    def __init__(self):
        self.mem = True
    
    def schedule(self, event_name, event_value, CLK):
        if event_name == 'REQ':
            Q = (not CLK) and (not self.mem)
            self.mem = not CLK
            return event_value, Q