import logging
class F_DINT_TO_SINT:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                val = int(IN) if not isinstance(IN, int) else IN
                val = val & 0xFF

                if val >= 128:
                    val = val - 256
                return event_value, val

            except Exception as e:
                logging.error("Error in F_DINT_TO_SINT: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_DINT_TO_SINT class destroyed')
