class E_SWITCH:
    def schedule(self, event_name, event_value, G):
        if event_name == 'EI':
            if not G:
                return event_value, None
            else:
                return None, event_value    
    def __del__(self):
        print('E_SWITCH class destroyed')