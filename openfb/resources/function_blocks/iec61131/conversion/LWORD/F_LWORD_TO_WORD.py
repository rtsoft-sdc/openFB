class F_LWORD_TO_WORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, int(IN) & 0xFFFF

    def __del__(self):
        print('F_LWORD_TO_WORD class destroyed')
