import math

class F_TAN:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, math.tan(IN)

    def __del__(self):
        print('F_TAN class destroyed')