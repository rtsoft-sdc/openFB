class F_ULINT_TO_REAL:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, float(int(IN) & 0xFFFFFFFFFFFFFFFF)

    def __del__(self):
        print('F_ULINT_TO_REAL class destroyed')
