class F_INT_TO_REAL:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, float(IN)