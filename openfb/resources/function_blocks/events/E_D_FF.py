class E_D_FF:
    def __init__(self):
        self.Q = False

    def schedule(self, event_name, event_value, D):
        if event_name == 'CLK':
            self.Q = D
            return event_value, self.Q