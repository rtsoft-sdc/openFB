class E_SELECT:
    def schedule(self, event_name, event_value, G):
        if event_name == 'EI0' and not G:
            return 'EO', event_value
        elif event_name == 'EI1' and G:
            return 'EO', event_value
        return None