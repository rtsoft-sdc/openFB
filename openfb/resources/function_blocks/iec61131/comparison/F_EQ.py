class F_EQ:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            return event_value, IN1 == IN2

    def __del__(self):
        print('F_EQ class destroyed')
