class F_INT_TO_BYTE:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, IN & 0xFF