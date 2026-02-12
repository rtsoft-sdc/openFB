class FB_CTUD:
    def __init__(self):
        self.cv = 0
    
    def schedule(self, event_name, event_value, CU, CD, R, LD, PV):
        if event_name == 'REQ':
            if R:
                self.cv = 0
            elif LD:
                self.cv = PV
            elif not (CU and CD):
                if CU and self.cv < 32767:
                    self.cv += 1
                elif CD and self.cv > -32768:
                    self.cv -= 1
            
            QU = self.cv >= PV
            QD = self.cv <= 0
            return event_value, QU, QD, self.cv