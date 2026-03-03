import logging
class OR_3:
    def schedule(self, event_name, event_value, IN1, IN2, IN3):
        if event_name == 'REQ':
            try:
                return event_value, int(IN1) | int(IN2) | int(IN3)

            except Exception as e:
                logging.error("Error in OR_3: %s", str(e))
                return event_value, None
            
    def __del__(self):
        logging.info('OR_3 class destroyed')
