class E_CTU:
    def __init__(self):
        self.CV = 0
        self.Q = False

    def schedule(self, event_name, event_value, PV):
        if event_name == 'CU':
            self.CV += 1
            self.Q = (self.CV >= PV) if PV is not None else False
            return event_value, self.Q, self.CV
        elif event_name == 'R':
            self.CV = 0
            self.Q = False
            return event_value, self.Q, self.CV
    
    def __del__(self):
        print('E_CTU class destroyed')
        