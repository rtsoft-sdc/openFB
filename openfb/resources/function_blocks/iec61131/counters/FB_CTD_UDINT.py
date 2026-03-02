class FB_CTD_UDINT:
    def __init__(self):
        self.cv = 0
    
    def schedule(self, event_name, event_value, CD, PV, LD):
        if event_name == 'REQ':
            if LD:
                self.cv = PV & 0xFFFFFFFF
            elif CD and self.cv > 0:
                self.cv -= 1
            Q = self.cv <= 0
            return event_value, Q, self.cv & 0xFFFFFFFF

    def __del__(self):
        print('FB_CTD_UDINT class destroyed')