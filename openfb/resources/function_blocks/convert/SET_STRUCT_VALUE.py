import logging
class SET_STRUCT_VALUE:
    def schedule(self, event_name, event_value, member, in_struct, element_value):
        if event_name == 'REQ':
            try:
                if isinstance(in_struct, dict):
                    out_struct = in_struct.copy()
                else:
                    import copy
                    out_struct = copy.copy(in_struct)
                
                parts = member.split('.')
                current = out_struct
                
                for part in parts[:-1]:
                    if isinstance(current, dict):
                        if part not in current:
                            current[part] = {}
                        current = current[part]
                    elif hasattr(current, '__dict__'):
                        if not hasattr(current, part):
                            setattr(current, part, {})
                        current = getattr(current, part)
                    else:
                        return event_value, False, in_struct
                
                final_member = parts[-1]
                if isinstance(current, dict):
                    current[final_member] = element_value
                elif hasattr(current, '__dict__'):
                    setattr(current, final_member, element_value)
                else:
                    return event_value, False, in_struct
                
                return event_value, True, out_struct
            except Exception:
                return event_value, False, None
    
    def __del__(self):
        logging.info('SET_STRUCT_VALUE class destroyed')
