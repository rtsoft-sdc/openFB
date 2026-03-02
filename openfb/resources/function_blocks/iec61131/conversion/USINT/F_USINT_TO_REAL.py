class F_USINT_TO_REAL:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, float(int(IN) & 0xFF)

    def __del__(self):
        print('F_USINT_TO_REAL class destroyed')
