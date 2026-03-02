import math

class F_EXP:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, math.exp(IN)

    def __del__(self):
        print('F_EXP class destroyed')