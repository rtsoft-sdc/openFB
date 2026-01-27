import logging

class THROUGH_BLOCK:
    def __del__(self):
        # cleanup logic
        logging.debug("Object is being destroyed")

    def schedule(self, event_name, event_value, BOOL_IN, BYTE_IN, DINT_IN, DWORD_IN, INT_IN,
                 LREAL_IN, REAL_IN, SINT_IN, STRING_IN, TIME_IN, UDINT_IN, UINT_IN,
                   USINT_IN, WORD_IN, WSTRING_IN):
       logging.info(
       "Inputs: bool_in=%s \nbyte_in=%s \ndint_in=%s \ndword_in=%s \nint_in=%s\n"
       "lreal_in=%s \nreal_in=%s \nsint_in=%s \nstring_in=%s \ntime_in=%s\n"
       "udint_in=%s \nuint_in=%s \nusint_in=%s \nword_in=%s \nwstring_in=%s",
       BOOL_IN, hex(BYTE_IN), DINT_IN, hex(DWORD_IN), INT_IN,
       LREAL_IN, REAL_IN, SINT_IN, STRING_IN, TIME_IN,
       UDINT_IN, UINT_IN, USINT_IN, hex(WORD_IN), WSTRING_IN
       )
        
       return event_value, BOOL_IN, BYTE_IN, DINT_IN, DWORD_IN, INT_IN, LREAL_IN, REAL_IN, SINT_IN, STRING_IN, TIME_IN, UDINT_IN, UINT_IN, USINT_IN, WORD_IN, WSTRING_IN