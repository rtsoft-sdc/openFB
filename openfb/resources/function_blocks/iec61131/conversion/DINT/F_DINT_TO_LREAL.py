class F_DINT_TO_LREAL:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            val = int(IN) if not isinstance(IN, int) else IN
            return event_value, float(val)

    def __del__(self):
        print('F_DINT_TO_LREAL class destroyed')
