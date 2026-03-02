class E_MUX_8:
    def schedule(self, event_name, event_value):
        mapping = {
            'EI1': 0,
            'EI2': 1,
            'EI3': 2,
            'EI4': 3,
            'EI5': 4,
            'EI6': 5,
            'EI7': 6,
            'EI8': 7
        }
        if event_name in mapping:
            return event_value, mapping[event_name]
    
    def __del__(self):
        print('E_MUX_8 class destroyed')