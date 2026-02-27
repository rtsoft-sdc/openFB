class F_LREAL_TO_ULINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, int(float(IN))
