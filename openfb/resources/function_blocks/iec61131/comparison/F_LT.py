class F_LT:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            return event_value, IN1 < IN2

    def __del__(self):
        print('F_LT class destroyed')
