import math

class F_SQRT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, math.sqrt(IN)

    def __del__(self):
        print('F_SQRT class destroyed')
