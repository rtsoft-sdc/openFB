import math

class F_LOG:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, math.log10(IN)

    def __del__(self):
        print('F_LOG class destroyed')
