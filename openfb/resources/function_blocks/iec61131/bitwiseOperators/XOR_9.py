import logging
class XOR_9:
    def schedule(self, event_name, event_value, IN1, IN2, IN3, IN4, IN5, IN6, IN7, IN8, IN9):
        if event_name == 'REQ':
            try:
                vals = (IN1,IN2,IN3,IN4,IN5,IN6,IN7,IN8,IN9)
                res = int(vals[0])
                for v in vals[1:]:
                    res ^= int(v)
                return event_value, res

            except Exception as e:
                logging.error("Error in XOR_9: %s", str(e))
                return event_value, None
            
    def __del__(self):
        logging.info('XOR_9 class destroyed')
