class SET_AT_INDEX:
    def schedule(self, event_name, event_value, IN_ARRAY, INDEX, VALUE):
        if event_name == 'REQ':
            try:
                if isinstance(IN_ARRAY, (list, tuple)) and 0 <= INDEX < len(IN_ARRAY):
                    OUT_ARRAY = list(IN_ARRAY)
                    OUT_ARRAY[INDEX] = VALUE
                    return event_value, True, OUT_ARRAY
                else:
                    return event_value, False, IN_ARRAY
            except Exception:
                return event_value, False, IN_ARRAY