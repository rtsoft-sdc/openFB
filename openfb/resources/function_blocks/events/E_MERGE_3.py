class E_MERGE_3:
    def schedule(self, event_name, event_value):
        if event_name in ['EI1', 'EI2', 'EI3']:
            return event_value
        return None