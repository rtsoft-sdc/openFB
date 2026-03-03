import logging
class E_MUX_2:
    def schedule(self, event_name, event_value):
        mapping = {
            'EI1': 0,
            'EI2': 1,
        }
        if event_name in mapping:
            return event_value, mapping[event_name]
    
    def __del__(self):
        logging.info('E_MUX_2 class destroyed')
        