class F_LWORD_BCD_TO_ULINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                val = int(IN) if not isinstance(IN, int) else IN
                result = 0
                multiplier = 1
                
                for i in range(16):
                    digit = (val >> (i * 4)) & 0x0F
                    if digit > 9:
                        return event_value, 0
                    result += digit * multiplier
                    multiplier *= 10
                
                return event_value, result
            except Exception:
                return None, 0
