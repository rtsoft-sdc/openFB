class F_INT_TO_WORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            val = int(IN)
            return event_value, val & 0xFFFF if val >= 0 else (val + 65536) & 0xFFFF

    def __del__(self):
        print('F_INT_TO_WORD class destroyed')