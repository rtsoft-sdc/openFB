class UDINT2UDINT:
    
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, IN