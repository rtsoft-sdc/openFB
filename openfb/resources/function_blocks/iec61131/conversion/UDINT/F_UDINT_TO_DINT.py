class F_UDINT_TO_DINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            val = int(IN) & 0xFFFFFFFF
            return event_value, val if val < 0x80000000 else val - 0x100000000

    def __del__(self):
        print('F_UDINT_TO_DINT class destroyed')
