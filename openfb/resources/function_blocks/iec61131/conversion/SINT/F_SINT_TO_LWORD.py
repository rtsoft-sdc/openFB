class F_SINT_TO_LWORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            val = int(IN)
            return event_value, val & 0xFF if val >= 0 else (val + 256) & 0xFFFFFFFFFFFFFFFF

    def __del__(self):
        print('F_SINT_TO_LWORD class destroyed')
