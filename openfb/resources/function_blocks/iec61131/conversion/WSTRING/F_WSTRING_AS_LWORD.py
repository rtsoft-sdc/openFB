class F_WSTRING_AS_LWORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, int(str(IN)) & 0xFFFFFFFFFFFFFFFF

    def __del__(self):
        print('F_WSTRING_AS_LWORD class destroyed')
