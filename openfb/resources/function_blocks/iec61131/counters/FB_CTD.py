class FB_CTD:
    def __init__(self):
        self.cv = 0
    
    def schedule(self, event_name, event_value, CD, LD, PV):
        if event_name == 'REQ':
            if LD:
                self.cv = PV
            elif CD and self.cv > -32768:
                self.cv -= 1
            Q = self.cv <= 0
            return event_value, Q, self.cv

    def __del__(self):
        print('FB_CTD class destroyed')