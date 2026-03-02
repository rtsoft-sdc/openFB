class F_USINT_AS_WSTRING:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, str(int(IN) & 0xFF)

    def __del__(self):
        print('F_USINT_AS_WSTRING class destroyed')
