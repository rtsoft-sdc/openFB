class F_STRING_AS_BOOL:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            s = str(IN).lower().strip()
            return event_value, s in ['true', '1']

    def __del__(self):
        print('F_STRING_AS_BOOL class destroyed')
