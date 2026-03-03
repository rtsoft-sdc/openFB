import logging
class VALUES_TO_ARRAY:
    def schedule(self, event_name, event_value, *inputs, **kwargs):
        if event_name == 'REQ':
            try:
                if kwargs:
                    out_array = list(kwargs.values())
                elif len(inputs) == 1 and isinstance(inputs[0], (list, tuple)):
                    out_array = list(inputs[0])
                elif len(inputs) == 1 and isinstance(inputs[0], dict):
                    out_array = list(inputs[0].values())
                else:
                    out_array = list(inputs)

                return event_value, out_array
            except Exception:
                return event_value, []
    
    def __del__(self):
        logging.info('VALUES_TO_ARRAY class destroyed')
