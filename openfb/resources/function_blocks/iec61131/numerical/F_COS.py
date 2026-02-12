import math

class F_COS:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, math.cos(IN)