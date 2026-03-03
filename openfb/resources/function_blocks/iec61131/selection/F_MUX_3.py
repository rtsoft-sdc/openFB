import logging
class F_MUX_3:
    def schedule(self, event_name, event_value, IN1, IN2, IN3, K):
        if event_name == 'REQ':
            try:
                if K == 0:
                    return event_value, IN1
                elif K == 1:
                    return event_value, IN2
                else: 
                    return event_value, IN3

            except Exception as e:
                logging.error("Error in F_MUX_3: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_MUX_3 class destroyed')