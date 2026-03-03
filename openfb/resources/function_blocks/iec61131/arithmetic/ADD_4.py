import logging
class ADD_4:
    def schedule(self, event_name, event_value, IN1, IN2, IN3, IN4):
        if event_name == 'REQ':
            try:
                return event_value, IN1 + IN2 + IN3 + IN4

            except Exception as e:
                logging.error("Error in ADD_4: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('ADD_4 class destroyed')
