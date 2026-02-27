import random
import time


class FB_RANDOM:
    def __init__(self):
        self.initialized = False
    
    def schedule(self, event_name, event_value, SEED):
        if event_name == 'INIT':
            if SEED == 0:
                random.seed(time.time())
            else:
                random.seed(SEED)
            self.initialized = True
            return event_value, None, None
        
        elif event_name == 'REQ':
            val = random.random()
            return None, event_value, val        
        return None, None, 0.0
