class F_DIVTIME:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':   
            #if not isinstance(IN2, (int, float)) \\ IN2!0???              
            return event_value, IN1/IN2
                