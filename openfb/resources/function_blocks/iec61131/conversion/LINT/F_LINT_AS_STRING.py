class F_LINT_AS_STRING:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, str(int(IN))

    def __del__(self):
        print('F_LINT_AS_STRING class destroyed')
