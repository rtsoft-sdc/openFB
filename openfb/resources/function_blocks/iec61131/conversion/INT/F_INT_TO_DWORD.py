class F_INT_TO_DWORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            val = int(IN)
            return event_value, val & 0xFFFF if val >= 0 else (val + 65536) & 0xFFFFFFFF