class FB_CTD_DINT:
    def __init__(self):
        self.cv = 0
    
    def schedule(self, event_name, event_value, CD, PV, LD):
        if event_name == 'REQ':
            if LD:
                self.cv = PV
            elif CD and self.cv > -2147483648:
                self.cv -= 1
            Q = self.cv <= 0
            return event_value, Q, self.cv