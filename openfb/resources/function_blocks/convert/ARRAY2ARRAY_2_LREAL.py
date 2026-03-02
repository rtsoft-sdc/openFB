class ARRAY2ARRAY_2_LREAL:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, [float(IN[0]), float(IN[1])]
    
    def __del__(self):
        print('ARRAY2ARRAY_2_LREAL class destroyed')