class F_BYTE_TO_UINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            val = int(IN) if not isinstance(IN, int) else IN
            return event_value, val & 0xFF

    def __del__(self):
        print('F_BYTE_TO_UINT class destroyed')
