class E_T_FF:
    def __init__(self):
        self.Q = False

    def schedule(self, event_name, event_value):
        if event_name == 'CLK':
            self.Q = not self.Q
            return event_value, self.Q
        return None
    
    def __del__(self):
        print('E_T_FF class destroyed')