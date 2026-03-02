import math

class F_ACOS:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, math.acos(IN)

    def __del__(self):
        print('F_ACOS class destroyed')