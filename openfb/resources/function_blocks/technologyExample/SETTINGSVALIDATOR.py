class SETTINGSVALIDATOR:
    def __init__(self):
        pass

    def schedule(self, event_input_name, event_input_value, CURRENTVALUE, DSPVALUEVEPOS, VALUELIML, VALUELIMH):
        if event_input_name == "REQ":
            if CURRENTVALUE is None or DSPVALUEVEPOS is None:
                return event_input_value, CURRENTVALUE, VALUELIML, VALUELIMH

            lim_l = VALUELIML if VALUELIML is not None else -1e9
            lim_h = VALUELIMH if VALUELIMH is not None else 1e9

            new_sp = CURRENTVALUE + DSPVALUEVEPOS

            if new_sp > lim_h:
                new_sp = lim_h
            elif new_sp < lim_l:
                new_sp = lim_l

            return event_input_value, round(new_sp, 4), lim_l, lim_h

        return event_input_value, CURRENTVALUE, VALUELIML, VALUELIMH