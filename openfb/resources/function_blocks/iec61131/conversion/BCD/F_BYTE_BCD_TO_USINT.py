import logging
class F_BYTE_BCD_TO_USINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                val = int(IN) if not isinstance(IN, int) else IN
                high = (val >> 4) & 0x0F
                low = val & 0x0F
                
                if high > 9 or low > 9:
                    return event_value, 0
                
                result = high * 10 + low
                return event_value, result
            except Exception as e:
                logging.error("Error in F_BYTE_BCD_TO_USINT: %s", str(e))
                return event_value, 0

    def __del__(self):
        logging.info('F_BYTE_BCD_TO_USINT class destroyed')
