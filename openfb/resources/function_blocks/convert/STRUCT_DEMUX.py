class STRUCT_DEMUX:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            
            if isinstance(IN, dict):
                OUT = IN
            elif hasattr(IN, '__dict__'):
                OUT = vars(IN)
            elif hasattr(IN, '_asdict'):
                OUT = IN._asdict()
            return event_value, OUT