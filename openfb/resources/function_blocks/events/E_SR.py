class E_SR:
    def __init__(self):
        self.Q = False

    def schedule(self, event_name, event_value):
        if event_name == 'S':
            self.Q = True
            return event_value, self.Q
        elif event_name == 'R':
            self.Q = False
            return event_value, self.Q
        return None