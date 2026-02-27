class F_INT_TO_SINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            byte_val = int(IN) & 0xFF
            return event_value, byte_val - 256 if byte_val >= 128 else byte_val 