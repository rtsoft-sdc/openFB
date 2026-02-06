class F_INT_TO_WORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, IN & 0xFFFF