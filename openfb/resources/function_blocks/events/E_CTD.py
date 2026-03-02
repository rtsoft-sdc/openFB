class E_CTD:
    def __init__(self):
        self.CV = 0
        self.Q = False

    def schedule(self, event_name, event_value, PV):
        if event_name == 'CD':
            if self.CV > 0:
                self.CV -= 1
            self.Q = (self.CV == 0)
            return event_value, self.Q, self.CV
        elif event_name == 'LD':
            self.CV = PV
            self.Q = (self.CV == 0)
            return event_value, self.Q, self.CV
    
    def __del__(self):
        print('E_CTD class destroyed')