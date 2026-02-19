class E_T_FF_SR:
    def __init__(self):
        self.Q = False

    def schedule(self, event_name, event_value):
        if event_name == 'S':
            self.Q = True
            return 'EO', self.Q
        elif event_name == 'R':
            self.Q = False
            return 'EO', self.Q
        elif event_name == 'CLK':
            self.Q = not self.Q
            return 'EO', self.Q
        return None