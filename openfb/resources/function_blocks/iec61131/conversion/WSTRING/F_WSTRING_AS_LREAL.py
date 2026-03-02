class F_WSTRING_AS_LREAL:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, float(str(IN))

    def __del__(self):
        print('F_WSTRING_AS_LREAL class destroyed')
