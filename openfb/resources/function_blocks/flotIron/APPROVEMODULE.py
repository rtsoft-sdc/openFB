class APPROVEMODULE:

    def __init__(self):
        self.SP = 3.8

    def schedule(self, event_input_name, event_input_value, CURRENTVALUE, DSPVALUEVEPOS, VALUELIML, VALUELIMH):
    
        if event_input_name == "REQ":
            if CURRENTVALUE is None or DSPVALUEVEPOS is None or VALUELIMH is None or VALUELIML is None:
                return event_input_value, self.SP, VALUELIML, VALUELIMH
            if self.SP + DSPVALUEVEPOS > VALUELIMH or self.SP + DSPVALUEVEPOS < VALUELIML:
                print(f"AAWAWAWAW")
                return event_input_value, self.SP, VALUELIML, VALUELIMH
            self.SP += DSPVALUEVEPOS
            return event_input_value, self.SP, VALUELIML, VALUELIMH