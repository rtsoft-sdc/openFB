import logging
class AND_2:
    def schedule(self, event_name, event_value, IN1, IN2):
        if event_name == 'REQ':
            try:
                return event_value, int(IN1) & int(IN2)

            except Exception as e:
                logging.error("Error in AND_2: %s", str(e))
                return event_value, None
            
    def __del__(self):
        logging.info('AND_2 class destroyed')
