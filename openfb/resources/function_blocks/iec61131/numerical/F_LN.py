import math

class F_LN:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, math.log(IN)

    def __del__(self):
        print('F_LN class destroyed')