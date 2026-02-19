class STRUCT_DEMUX:
    #need to remake 
    def schedule(self, event_name, event_value, **kwargs):
        if event_name == 'REQ':
            try:
                in_struct = kwargs.get('IN')
                if in_struct is None:
                    return event_value
                
                return event_value
            except Exception:
                return event_value
