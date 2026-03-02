class E_SPLIT_2:
    def schedule(self, event_name, event_value):
        if event_name == 'EI':
            return [event_value, event_value]
        return None
    
    def __del__(self):
        print('E_SPLIT_2 class destroyed')