class F_INT_TO_UDINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, IN & 0xFFFFFFFF