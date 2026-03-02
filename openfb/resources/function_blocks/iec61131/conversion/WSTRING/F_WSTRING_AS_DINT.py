class F_WSTRING_AS_DINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, int(str(IN))

    def __del__(self):
        print('F_WSTRING_AS_DINT class destroyed')
