import time
import logging

class SLEEP:
    def __del__(self):
        # cleanup logic
        logging.debug("Object is being destroyed")

    def schedule(self, event_name, event_value):
        if event_name == 'SLEEP':
            # time.sleep(0.01)
            return [event_value]

