class F_SINT_TO_ULINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            val = int(IN)
            return event_value, val if val >= 0 else val + 256
