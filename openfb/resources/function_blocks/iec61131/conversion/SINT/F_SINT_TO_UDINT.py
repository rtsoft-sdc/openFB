import logging
class F_SINT_TO_UDINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                val = int(IN)
                return event_value, val if val >= 0 else val + 256

            except Exception as e:
                logging.error("Error in F_SINT_TO_UDINT: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_SINT_TO_UDINT class destroyed')
