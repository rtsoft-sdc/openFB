class F_UINT_AS_WSTRING:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, str(int(IN) & 0xFFFF)

    def __del__(self):
        print('F_UINT_AS_WSTRING class destroyed')
