class ADD_4:
    def schedule(self, event_name, event_value, IN1, IN2, IN3, IN4):
        if event_name == 'REQ':
            return event_value, IN1 + IN2 + IN3 + IN4

    def __del__(self):
        print('ADD_4 class destroyed')
