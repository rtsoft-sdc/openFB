class F_BYTE_TO_SINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            val = int(IN) if not isinstance(IN, int) else IN
            val = val & 0xFF
            if val >= 128:
                val = val - 256
            return event_value, val
