import logging
class GET_STRUCT_VALUE:
    def schedule(self, event_name, event_value, member, in_struct):
        if event_name == 'REQ':
            try:
                value = in_struct
                for part in member.split('.'):
                    if isinstance(value, dict):
                        value = value.get(part)
                    elif hasattr(value, '__dict__'):
                        value = getattr(value, part, None)
                    elif hasattr(value, part): 
                        value = getattr(value, part)
                    else:
                        return None, False, None
                
                return event_value, True, value
            except Exception:
                return event_value, False, None
    
    def __del__(self):
        logging.info('GET_STRUCT_VALUE class destroyed')
            