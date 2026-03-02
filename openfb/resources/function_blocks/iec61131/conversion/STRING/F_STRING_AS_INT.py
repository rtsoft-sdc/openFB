class F_STRING_AS_INT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, int(str(IN))

    def __del__(self):
        print('F_STRING_AS_INT class destroyed')
