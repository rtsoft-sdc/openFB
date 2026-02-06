class F_INT_AS_WSTRING:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, str(IN)