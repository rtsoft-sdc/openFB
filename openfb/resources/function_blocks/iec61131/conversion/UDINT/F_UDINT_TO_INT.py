class F_UDINT_TO_INT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            val = int(IN) & 0xFFFF
            return event_value, val if val < 32768 else val - 65536
