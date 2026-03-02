class F_BOOL_TO_LINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, 1 if IN else 0

    def __del__(self):
        print('F_BOOL_TO_LINT class destroyed')
