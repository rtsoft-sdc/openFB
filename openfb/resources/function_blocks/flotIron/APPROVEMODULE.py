class APPROVEMODULE:

    def schedule(self, event_input_name, event_input_value, CURRENTVALUE, DSPVALUEVEPOS, VALUELIML, VALUELIMH):
    
        if event_input_name == "REQ":
            if CURRENTVALUE is None or DSPVALUEVEPOS is None or VALUELIMH is None or VALUELIML is None:
                return event_input_value, 0.0, 0.0, 0.0
            return event_input_value, DSPVALUEVEPOS, VALUELIML, VALUELIMH