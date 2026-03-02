class E_SELECT:
    def schedule(self, event_name, event_value, G):
        if event_name == 'EI0' and not G:
            return event_value
        elif event_name == 'EI1' and G:
            return event_value
        return None
    
    def __del__(self):
        print('E_SELECT class destroyed')