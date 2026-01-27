import random
import logging



class GENERATE_TWO_RANDOM:
    def __del__(self):
        # cleanup logic
        logging.debug("Object is being destroyed")

    def schedule(self, event_name, event_value, range):
        if event_name == 'INIT':
            return [event_value, None, 0, 0]

        elif event_name == 'RUN':
            rand1 = random.randrange(int(range))    
            rand2 = random.randrange(int(range))
            return [None, event_value, rand1, rand2]
