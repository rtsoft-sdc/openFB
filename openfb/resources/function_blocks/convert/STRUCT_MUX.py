class STRUCT_MUX:
    def schedule(self, event_name, event_value, *inputs, **kwargs):
        if event_name == 'REQ':
            try:
                if kwargs:
                    out_struct = dict(kwargs)
                elif len(inputs) == 1 and isinstance(inputs[0], dict):
                    out_struct = inputs[0].copy()
                elif len(inputs) == 1 and hasattr(inputs[0], '__dict__'):
                    out_struct = dict(vars(inputs[0]))
                else:
                    out_struct = {f"field{index + 1}": value for index, value in enumerate(inputs)}

                return event_value, out_struct
            except Exception:
                return None, {}
