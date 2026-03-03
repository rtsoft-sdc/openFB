import logging
class F_ULINT_TO_BCD_LWORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                val = int(IN) if not isinstance(IN, int) else IN
                if val > 9999999999999999 or val < 0:
                    return event_value, 0
                
                result = 0
                for i in range(16):
                    digit = val % 10
                    result |= (digit << (i * 4))
                    val //= 10
                
                return event_value, result
            except Exception as e:
                logging.error("Error in F_ULINT_TO_BCD_LWORD: %s", str(e))
                return event_value, 0

    def __del__(self):
        logging.info('F_ULINT_TO_BCD_LWORD class destroyed')
