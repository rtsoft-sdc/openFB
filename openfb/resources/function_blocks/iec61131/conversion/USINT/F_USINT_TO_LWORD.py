class F_USINT_TO_LWORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, int(IN) & 0xFF

    def __del__(self):
        print('F_USINT_TO_LWORD class destroyed')
