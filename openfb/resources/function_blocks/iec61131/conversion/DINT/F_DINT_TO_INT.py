class F_DINT_TO_INT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            val = int(IN) if not isinstance(IN, int) else IN
            val = val & 0xFFFF
            if val >= 32768:
                val = val - 65536
            return event_value, val
