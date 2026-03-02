class FB_CTU_DINT:
    def __init__(self):
        self.cv = 0
    
    def schedule(self, event_name, event_value, CU, R, PV):
        if event_name == 'REQ':
            if R:
                self.cv = 0
            elif CU and self.cv < 2147483647:
                self.cv += 1
            Q = self.cv >= PV
            return event_value, Q, self.cv

    def __del__(self):
        print('FB_CTU_DINT class destroyed')