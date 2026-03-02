class FB_CTD_LINT:
    def __init__(self):
        self.cv = 0
    
    def schedule(self, event_name, event_value, CD, PV, LD):
        if event_name == 'REQ':
            if LD:
                self.cv = PV
            elif CD and self.cv > -9223372036854775808:
                self.cv -= 1
            Q = self.cv <= 0
            return event_value, Q, self.cv

    def __del__(self):
        print('FB_CTD_LINT class destroyed')