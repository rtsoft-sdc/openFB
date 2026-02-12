class FB_CTU:
    def __init__(self):
        self.cv = 0
    
    def schedule(self, event_name, event_value, CU, R, PV):
        if event_name == 'REQ':
            if R:
                self.cv = 0
            elif CU and self.cv < 32767:
                self.cv += 1
            Q = self.cv >= PV
            return event_value, Q, self.cv