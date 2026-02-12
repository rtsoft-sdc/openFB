class FB_CTUD_LINT:
    def __init__(self):
        self.cv = 0
    
    def schedule(self, event_name, event_value, CU, CD, R, LD, PV):
        if event_name == 'REQ':
            if R:
                self.cv = 0
            elif LD:
                self.cv = PV
            elif not (CU and CD):
                if CU and self.cv < 9223372036854775807:
                    self.cv += 1
                elif CD and self.cv > -9223372036854775808:
                    self.cv -= 1
            
            QU = self.cv >= PV
            QD = self.cv <= 0
            return event_value, QU, QD, self.cv