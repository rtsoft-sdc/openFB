class STRUCT_DEMUX:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                if isinstance(IN, dict):
                    values = list(IN.values())
                elif hasattr(IN, '__dict__'):
                    values = list(vars(IN).values())
                elif isinstance(IN, (list, tuple)):
                    values = list(IN)
                else:
                    return event_value

                return tuple([event_value] + values)
            except Exception:
                return None
