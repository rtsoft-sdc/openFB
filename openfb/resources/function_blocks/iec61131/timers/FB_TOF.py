import logging
import time
from datetime import timedelta
from ...datetime_parsing import parse_time_interval


class FB_TOF:
    def __init__(self):
        self.start_time = None
        self.prev_in = False
        self.q = False
    
    def schedule(self, event_name, event_value, IN, PT):
        if event_name == 'REQ':
            try:
                now = time.monotonic()
                pt_delta = parse_time_interval(PT)
                PT_seconds = pt_delta.total_seconds()
                
                if IN and not self.prev_in:
                    self.q = True
                    self.start_time = None
                if not IN and self.prev_in:
                    self.start_time = now
                
                self.prev_in = IN
                
                if IN:
                    ET = timedelta(0)
                else:
                    if self.start_time is None:
                        ET = timedelta(0)
                    else:
                        elapsed_seconds = now - self.start_time
                        if elapsed_seconds < PT_seconds:
                            self.q = True
                            ET = timedelta(seconds=elapsed_seconds)
                        else:
                            self.q = False
                            ET = pt_delta
                
                return event_value, self.q, ET

            except Exception as e:
                logging.error("Error in FB_TOF: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('FB_TOF class destroyed')