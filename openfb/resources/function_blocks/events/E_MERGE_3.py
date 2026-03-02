class E_MERGE_3:
    def schedule(self, event_name, event_value):
        if event_name in ['EI1', 'EI2', 'EI3']:
            return event_value
        return None
    
    def __del__(self):
        print('E_MERGE_3 class destroyed')