class F_USINT_TO_BCD_BYTE:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                val = int(IN) if not isinstance(IN, int) else IN
                if val > 99 or val < 0:
                    return event_value, 0
                
                high = (val // 10) & 0x0F
                low = (val % 10) & 0x0F
                result = (high << 4) | low
                
                return event_value, result
            except Exception:
                return None, 0
