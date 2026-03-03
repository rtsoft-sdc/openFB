import logging
class OR_6:
    def schedule(self, event_name, event_value, IN1, IN2, IN3, IN4, IN5, IN6):
        if event_name == 'REQ':
            try:
                res = int(IN1)
                for v in (IN2, IN3, IN4, IN5, IN6):
                    res |= int(v)
                return event_value, res

            except Exception as e:
                logging.error("Error in OR_6: %s", str(e))
                return event_value, None
            
    def __del__(self):
        logging.info('OR_6 class destroyed')
