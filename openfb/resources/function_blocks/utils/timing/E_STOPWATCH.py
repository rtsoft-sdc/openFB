import logging
import time


class E_STOPWATCH:
    def __init__(self):
        self.start_time = None
        self.td = 0
        
    def schedule(self, event_name, event_value):
        if event_name == 'START':
            self.start_time = time.monotonic()
            return event_value, None, None, self.td
            
        elif event_name == 'ET':
            if self.start_time is not None:
                self.td = int((time.monotonic() - self.start_time) * 1000)  # в миллисекундах
            return None, event_value, None, self.td
            
        elif event_name == 'STOP':
            if self.start_time is not None:
                self.td = int((time.monotonic() - self.start_time) * 1000)  # в миллисекундах
            return event_value, None, None, self.td
            
        elif event_name == 'RESET':
            self.start_time = None
            self.td = 0
            return None, None, event_value, self.td
            

    def __del__(self):
        logging.info('class destroyed')
