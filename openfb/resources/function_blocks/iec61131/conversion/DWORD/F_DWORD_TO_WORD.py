class F_DWORD_TO_WORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            val = int(IN) if not isinstance(IN, int) else IN
            return event_value, val & 0xFFFF

    def __del__(self):
        print('F_DWORD_TO_WORD class destroyed')
