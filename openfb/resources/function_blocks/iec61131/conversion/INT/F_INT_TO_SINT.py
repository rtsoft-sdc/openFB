class F_INT_TO_SINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, IN 