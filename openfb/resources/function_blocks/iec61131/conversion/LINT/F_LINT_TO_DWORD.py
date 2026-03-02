class F_LINT_TO_DWORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, int(IN) & 0xFFFFFFFF

    def __del__(self):
        print('F_LINT_TO_DWORD class destroyed')
