import logging
class F_RIGHT:
    def schedule(self, event_name, event_value, IN, L):
        if event_name == 'REQ':
            try:
                s = str(IN)
                n = int(L)

                if n <= 0:
                    return None, ''
                return event_value, s[-n:]

            except Exception as e:
                logging.error("Error in F_RIGHT: %s", str(e))
                return event_value, None
            
    def __del__(self):
        logging.info('F_RIGHT class destroyed')
