class APPEND_STRING_2:
    def schedule(self, event_name, event_value, IN_1, IN_2):
        if event_name == 'REQ':
            return event_value, str(IN_1) + str(IN_2)