class ConvertBase:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            print(f"ConvertBase.schedule: {event_name}, {event_value}, {IN}")
            return event_value, IN
        return event_value, None
