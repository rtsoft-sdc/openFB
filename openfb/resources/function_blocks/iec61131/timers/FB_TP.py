import logging
import time
from datetime import timedelta
from ...datetime_parsing import parse_time_interval


class FB_TP:
    def __init__(self):
        self.start_time = None
        self.prev_in = False
        self.q = False
        self.pulse_active = False
    
    def schedule(self, event_name, event_value, IN, PT):
        if event_name == 'REQ':
            try:
                now = time.monotonic()
                pt_delta = parse_time_interval(PT)
                PT_seconds = pt_delta.total_seconds()
                
                if not self.prev_in and IN and not self.pulse_active:
                    self.start_time = now
                    self.pulse_active = True
                    self.q = True
                
                self.prev_in = IN
                
                if self.pulse_active and self.start_time is not None:
                    elapsed = now - self.start_time
                    if elapsed < PT_seconds:
                        self.q = True
                        ET = timedelta(seconds=elapsed)
                    else:
                        self.q = False
                        self.pulse_active = False
                        ET = pt_delta
                else:
                    self.q = False
                    ET = timedelta(0)
                
                return event_value, self.q, ET

            except Exception as e:
                logging.error("Error in FB_TP: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('FB_TP class destroyed')