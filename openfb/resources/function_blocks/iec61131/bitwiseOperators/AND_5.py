class AND_5:
    def schedule(self, event_name, event_value, IN1, IN2, IN3, IN4, IN5):
        if event_name == 'REQ':
            return event_value, int(IN1) & int(IN2) & int(IN3) & int(IN4) & int(IN5)

    def __del__(self):
        print('AND_5 class destroyed')
