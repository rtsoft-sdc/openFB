class AND_3:
    def schedule(self, event_name, event_value, IN1, IN2, IN3):
        if event_name == 'REQ':
            return event_value, int(IN1) & int(IN2) & int(IN3)

    def __del__(self):
        print('AND_3 class destroyed')
