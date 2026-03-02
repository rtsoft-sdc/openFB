class F_BOOL_TO_SINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, 1 if IN else 0

    def __del__(self):
        print('F_BOOL_TO_SINT class destroyed')
