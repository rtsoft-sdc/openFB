class E_REND:
    def __init__(self):
        self.ei1 = False
        self.ei2 = False

    def schedule(self, event_name, event_value):
        if event_name == 'EI1':
            self.ei1 = True
        elif event_name == 'EI2':
            self.ei2 = True
        elif event_name == 'R':
            self.ei1 = False
            self.ei2 = False
            return None
        if self.ei1 and self.ei2:
            self.ei1 = False
            self.ei2 = False
            return event_value
        return None