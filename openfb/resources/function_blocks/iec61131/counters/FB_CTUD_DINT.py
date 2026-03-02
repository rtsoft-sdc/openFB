class FB_CTUD_DINT:
    def __init__(self):
        self.cv = 0
    
    def schedule(self, event_name, event_value, CU, CD, R, LD, PV):
        if event_name == 'REQ':
            if R:
                self.cv = 0
            elif LD:
                self.cv = PV
            elif not (CU and CD):
                if CU and self.cv < 2147483647:
                    self.cv += 1
                elif CD and self.cv > -2147483648:
                    self.cv -= 1
            
            QU = self.cv >= PV
            QD = self.cv <= 0
            return event_value, QU, QD, self.cv

    def __del__(self):
        print('FB_CTUD_DINT class destroyed')