import logging
class F_ROR:
    def schedule(self, event_name, event_value, IN, N, WIDTH=32):
        if event_name == 'REQ':
            try:
                val = int(IN)
                n = int(N) % WIDTH
                mask = (1 << WIDTH) - 1
                res = ((val & mask) >> n) | ((val << (WIDTH - n)) & mask)
                return event_value, res    

            except Exception as e:
                logging.error("Error in F_ROR: %s", str(e))
                return event_value, None
            
    def __del__(self):
        logging.info('F_ROR class destroyed')
