class F_LWORD_TO_LINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            val = int(IN) & 0xFFFFFFFFFFFFFFFF
            return event_value, val if val < 0x8000000000000000 else val - 0x10000000000000000
