class F_UDINT_TO_SINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            val = int(IN) & 0xFF
            return event_value, val if val < 128 else val - 256
