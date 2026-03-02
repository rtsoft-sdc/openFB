class F_STRING_AS_UINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, int(str(IN)) & 0xFFFF

    def __del__(self):
        print('F_STRING_AS_UINT class destroyed')
