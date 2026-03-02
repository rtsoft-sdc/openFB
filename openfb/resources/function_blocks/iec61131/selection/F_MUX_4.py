class F_MUX_4:
    def schedule(self, event_name, event_value, IN1, IN2, IN3, IN4, K):
        if event_name == 'REQ':
            if K == 0:
                return event_value, IN1
            elif K == 1:
                return event_value, IN2
            elif K == 2:
                return event_value, IN3
            else:  # K == 3
                return event_value, IN4

    def __del__(self):
        print('F_MUX_4 class destroyed')