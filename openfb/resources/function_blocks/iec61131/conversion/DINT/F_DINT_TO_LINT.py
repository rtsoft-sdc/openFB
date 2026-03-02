class F_DINT_TO_LINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            val = int(IN) if not isinstance(IN, int) else IN
            if val >= 2147483648:
                val = val - 4294967296
            return event_value, val

    def __del__(self):
        print('F_DINT_TO_LINT class destroyed')
