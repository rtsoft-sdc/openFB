class F_LINT_TO_LWORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, int(IN) & 0xFFFFFFFFFFFFFFFF
