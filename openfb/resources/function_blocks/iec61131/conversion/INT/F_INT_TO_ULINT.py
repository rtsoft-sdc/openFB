class F_INT_TO_ULINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            val = int(IN)
            return event_value, val if val >= 0 else val + 65536

    def __del__(self):
        print('F_INT_TO_ULINT class destroyed')