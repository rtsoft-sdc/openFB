class F_WORD_TO_DWORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, int(IN) & 0xFFFF

    def __del__(self):
        print('F_WORD_TO_DWORD class destroyed')
