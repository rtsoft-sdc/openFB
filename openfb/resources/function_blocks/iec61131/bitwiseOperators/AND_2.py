class AND_2:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            return event_value, int(IN1) & int(IN2)

    def __del__(self):
        print('AND_2 class destroyed')
