import logging
class F_INT_TO_SINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                byte_val = int(IN) & 0xFF
                return event_value, byte_val - 256 if byte_val >= 128 else byte_val 

            except Exception as e:
                logging.error("Error in F_INT_TO_SINT: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_INT_TO_SINT class destroyed')