class F_TRUNC:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, int(IN)

    def __del__(self):
        print('F_TRUNC class destroyed')