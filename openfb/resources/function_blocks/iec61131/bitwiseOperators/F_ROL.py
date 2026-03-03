import logging
class F_ROL:
    def schedule(self, event_name, event_value, IN, N, WIDTH=32):
        if event_name == 'REQ':
            try:
                val = int(IN)
                n = int(N) % WIDTH
                mask = (1 << WIDTH) - 1
                res = ((val << n) & mask) | ((val & mask) >> (WIDTH - n))
                return event_value, res

            except Exception as e:
                logging.error("Error in F_ROL: %s", str(e))
                return event_value, None
            
    def __del__(self):
        logging.info('F_ROL class destroyed')
