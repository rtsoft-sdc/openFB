import logging

class OUT_ANY_CONSOLE:
    def schedule(self, event_name, event_value, QI, LABEL, IN):
        if event_name == 'REQ' and QI:
            if LABEL:
                logging.info(f"[{LABEL}] {IN}")
            else:
                logging.info(IN)
            return event_value, True

    def __del__(self):
        logging.info('class destroyed')