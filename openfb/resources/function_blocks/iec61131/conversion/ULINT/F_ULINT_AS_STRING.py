class F_ULINT_AS_STRING:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, str(int(IN) & 0xFFFFFFFFFFFFFFFF)

    def __del__(self):
        print('F_ULINT_AS_STRING class destroyed')
