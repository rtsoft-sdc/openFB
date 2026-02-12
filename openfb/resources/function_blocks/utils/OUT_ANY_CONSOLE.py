class OUT_ANY_CONSOLE:
    def schedule(self, event_name, event_value, QI, IN, LABEL=""):
        if event_name == 'REQ' and QI:
            if LABEL:
                print(f"[{LABEL}] {IN}")
            else:
                print(IN)
            return event_value, True