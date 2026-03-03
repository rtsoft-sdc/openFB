import logging
class XOR_7:
    def schedule(self, event_name, event_value, IN1, IN2, IN3, IN4, IN5, IN6, IN7):
        if event_name == 'REQ':
            try:
                res = int(IN1)
                for v in (IN2, IN3, IN4, IN5, IN6, IN7):
                    res ^= int(v)
                return event_value, res

            except Exception as e:
                logging.error("Error in XOR_7: %s", str(e))
                return event_value, None
            
    def __del__(self):
        logging.info('XOR_7 class destroyed')
