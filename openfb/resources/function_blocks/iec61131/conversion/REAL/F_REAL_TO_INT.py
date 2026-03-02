class F_REAL_TO_INT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                return event_value, int(float(IN))
            except:
                return event_value, None
        return event_value, None 

    def __del__(self):
        print('F_REAL_TO_INT class destroyed')