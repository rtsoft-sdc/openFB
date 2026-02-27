class F_DWORD_AS_WSTRING:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, str(int(IN) if not isinstance(IN, int) else IN)
