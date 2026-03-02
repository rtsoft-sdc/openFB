class F_SINT_TO_UINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            val = int(IN)
            return event_value, val if val >= 0 else val + 256

    def __del__(self):
        print('F_SINT_TO_UINT class destroyed')
