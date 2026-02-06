class STRUCT_MUX:
    
    def schedule(self, event_name, event_value, **fields):
        if event_name == 'REQ':
            OUT = fields
            return event_value, OUT