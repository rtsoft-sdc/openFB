class E_DELAY:
    def schedule(self, event_name, event_value, DT):
        if event_name == 'START':
            return event_value
        elif event_name == 'STOP':
            return None
        return None