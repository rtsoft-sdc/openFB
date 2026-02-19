class E_SPLIT_3:
    def schedule(self, event_name, event_value):
        if event_name == 'EI':
            return [event_value, event_value, event_value]
        return None