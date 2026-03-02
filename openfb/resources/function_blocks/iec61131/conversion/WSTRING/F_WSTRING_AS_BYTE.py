class F_WSTRING_AS_BYTE:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, int(str(IN)) & 0xFF

    def __del__(self):
        print('F_WSTRING_AS_BYTE class destroyed')
