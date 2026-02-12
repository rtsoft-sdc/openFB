import math

class F_SIN:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, math.sin(IN)
