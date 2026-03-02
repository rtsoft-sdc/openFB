class F_WSTRING_TO_STRING:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, str(IN)

    def __del__(self):
        print('F_WSTRING_TO_STRING class destroyed')
