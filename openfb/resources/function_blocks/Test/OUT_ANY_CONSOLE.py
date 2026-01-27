import time
import logging

class OUT_ANY_CONSOLE:
    def __del__(self):
        # cleanup logic
        logging.debug("Object is being destroyed")
    def schedule(self, event_name, event_value, QI, LABEL, IN):
        # if event_name == 'INIT':
        #     event_name = 'REQ'
        if event_name == 'REQ' and QI == True:
            logging.info(f"T#{time.time()}\tINFO: {LABEL}: {IN}")
            return event_value, 1
