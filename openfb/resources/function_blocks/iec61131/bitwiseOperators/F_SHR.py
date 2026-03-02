class F_SHR:
    def schedule(self, event_name, event_value, IN, N):
        if event_name == 'REQ':
            return event_value, int(IN) >> int(N)


    def __del__(self):
        print('F_SHR class destroyed')
