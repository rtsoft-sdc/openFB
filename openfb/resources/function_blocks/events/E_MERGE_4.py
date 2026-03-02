class E_MERGE_4:
    def schedule(self, event_name, event_value):
        if event_name in ['EI1', 'EI2', 'EI3', 'EI4']:
            return event_value
        return None
    
    def __del__(self):
        print('E_MERGE_4 class destroyed')