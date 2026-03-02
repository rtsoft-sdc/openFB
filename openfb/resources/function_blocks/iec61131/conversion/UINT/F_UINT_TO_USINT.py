class F_UINT_TO_USINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, int(IN) & 0xFF

    def __del__(self):
        print('F_UINT_TO_USINT class destroyed')
