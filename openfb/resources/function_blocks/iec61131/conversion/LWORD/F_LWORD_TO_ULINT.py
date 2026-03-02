class F_LWORD_TO_ULINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, int(IN) & 0xFFFFFFFFFFFFFFFF

    def __del__(self):
        print('F_LWORD_TO_ULINT class destroyed')
