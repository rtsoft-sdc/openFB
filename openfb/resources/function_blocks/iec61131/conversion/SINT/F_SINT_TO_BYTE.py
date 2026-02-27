class F_SINT_TO_BYTE:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            val = int(IN)
            return event_value, val & 0xFF if val >= 0 else (val + 256) & 0xFF
