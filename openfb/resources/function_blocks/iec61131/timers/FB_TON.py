import logging
import time
from datetime import timedelta
from openfb.data_model_fboot.datetime_parser import parse_time_interval


class FB_TON:
    def __init__(self):
        self.start_time = None
        self.q = False
    
    def schedule(self, event_name, event_value, IN, PT):
        if event_name == 'REQ':
            try:
                now = time.monotonic()
                pt_delta = parse_time_interval(PT)
                PT_seconds = pt_delta.total_seconds()
                
                if IN:
                    if self.start_time is None:
                        self.start_time = now
                    
                    elapsed = now - self.start_time
                    ET = timedelta(seconds=min(elapsed, PT_seconds))
                    
                    self.q = elapsed >= PT_seconds
                else:
                    self.start_time = None
                    self.q = False
                    ET = timedelta(0)
                
                return event_value, self.q, ET

            except Exception as e:
                logging.error("Error in FB_TON: %s", str(e))
                return event_value, None, None
    def __del__(self):
        logging.info('FB_TON class destroyed')