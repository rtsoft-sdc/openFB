class F_REAL_TO_SINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, int(float(IN))

    def __del__(self):
        print('F_REAL_TO_SINT class destroyed')
