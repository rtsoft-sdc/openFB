class F_LREAL_TO_REAL:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, float(IN)

    def __del__(self):
        print('F_LREAL_TO_REAL class destroyed')
