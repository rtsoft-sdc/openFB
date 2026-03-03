import logging
class XOR_5:
    def schedule(self, event_name, event_value, IN1, IN2, IN3, IN4, IN5):
        if event_name == 'REQ':
            try:
                res = int(IN1)
                for v in (IN2, IN3, IN4, IN5):
                    res ^= int(v)
                return event_value, res

            except Exception as e:
                logging.error("Error in XOR_5: %s", str(e))
                return event_value, None
            
    def __del__(self):
        logging.info('XOR_5 class destroyed')
