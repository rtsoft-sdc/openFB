class F_RIGHT:
    def schedule(self, event_name, event_value, IN, L):
        if event_name == 'REQ':
            s = str(IN)
            n = int(L)

            if n <= 0:
                return None, ''
            return event_value, s[-n:]

    def __del__(self):
        print('F_RIGHT class destroyed')
