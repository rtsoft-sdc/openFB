class F_LREAL_TO_DINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, int(float(IN))

    def __del__(self):
        print('F_LREAL_TO_DINT class destroyed')
