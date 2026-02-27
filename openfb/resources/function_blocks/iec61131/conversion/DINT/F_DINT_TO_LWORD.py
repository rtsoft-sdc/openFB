class F_DINT_TO_LWORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            val = int(IN) if not isinstance(IN, int) else IN
            return event_value, val & 0xFFFFFFFF
