class F_UDINT_TO_LREAL:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, float(int(IN) & 0xFFFFFFFF)

    def __del__(self):
        print('F_UDINT_TO_LREAL class destroyed')
