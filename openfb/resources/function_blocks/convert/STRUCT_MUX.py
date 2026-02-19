class STRUCT_MUX:
    def schedule(self, event_name, event_value, **kwargs):
        if event_name == 'REQ':
            try:
                out_struct = {}
                member_index = 0
                for key, value in kwargs.items():
                    if key not in ['event_name', 'event_value']:
                        out_struct[member_index] = value
                        member_index += 1

                return event_value, out_struct
            except Exception:
                return event_value, {}
