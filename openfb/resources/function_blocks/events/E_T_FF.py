class E_T_FF:
    def __init__(self):
        self.Q = False

    def schedule(self, event_name, event_value):
        if event_name == 'CLK':
            self.Q = not self.Q
            return 'EO', self.Q
        return None