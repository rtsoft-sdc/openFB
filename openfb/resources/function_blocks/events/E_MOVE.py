class E_MOVE:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, IN
    
    def __del__(self):
        print('E_MOVE class destroyed')