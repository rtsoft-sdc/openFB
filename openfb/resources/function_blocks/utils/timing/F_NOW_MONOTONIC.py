import logging
import time

class F_NOW_MONOTONIC:
    def schedule(self, event_name, event_value):
        if event_name == 'REQ':
            monotonic_time = int(time.monotonic() * 1000)
            return event_value, monotonic_time
        
    def __del__(self):
        logging.info('class destroyed')
