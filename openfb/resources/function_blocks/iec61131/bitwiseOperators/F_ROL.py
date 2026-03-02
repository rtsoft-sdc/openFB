class F_ROL:
    def schedule(self, event_name, event_value, IN, N, WIDTH=32):
        if event_name == 'REQ':
            val = int(IN)
            n = int(N) % WIDTH
            mask = (1 << WIDTH) - 1
            res = ((val << n) & mask) | ((val & mask) >> (WIDTH - n))
            return event_value, res


    def __del__(self):
        print('F_ROL class destroyed')
