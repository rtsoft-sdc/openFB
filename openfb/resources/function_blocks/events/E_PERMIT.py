class E_PERMIT:
    def schedule(self, event_name, event_value, PERMIT):
        if event_name == 'EI' and PERMIT:
            return event_value
        return None
    
    def __del__(self):
        print('E_PERMIT class destroyed')