class F_SINT_TO_INT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, int(IN)

    def __del__(self):
        print('F_SINT_TO_INT class destroyed')
