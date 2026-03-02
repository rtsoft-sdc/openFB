class F_FIND:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            s = '' if IN1 is None else str(IN1)
            sub = '' if IN2 is None else str(IN2)
            if sub == '':
                return event_value, 1 if s != '' else 0
            idx = s.find(sub)
            return event_value, 0 if idx == -1 else idx + 1

    def __del__(self):
        print('F_FIND class destroyed')
