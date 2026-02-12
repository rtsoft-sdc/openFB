import math

class F_ATAN:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, math.atan(IN)