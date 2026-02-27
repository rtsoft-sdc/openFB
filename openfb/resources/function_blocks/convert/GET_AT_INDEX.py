class GET_AT_INDEX:
    def schedule(self, event_name, event_value, IN_ARRAY, INDEX):
        if event_name == 'REQ':
            try:
                if isinstance(IN_ARRAY, (list, tuple)) and 0 <= INDEX < len(IN_ARRAY):
                    return event_value, True, IN_ARRAY[INDEX]
                else:
                    return event_value, False, None
            except Exception:
                return None, False, None