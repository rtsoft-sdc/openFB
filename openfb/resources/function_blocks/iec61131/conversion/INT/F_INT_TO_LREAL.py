class F_INT_TO_LREAL:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, float(int(IN)) 

    def __del__(self):
        print('F_INT_TO_LREAL class destroyed')