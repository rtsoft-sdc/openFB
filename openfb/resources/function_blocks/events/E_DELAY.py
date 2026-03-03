import logging
import time

class E_DELAY:
    
    def __init__(self):
        self._stop_requested = False
    
    def schedule(self, event_name, event_value, DT):
        if event_name == 'START':
            try:
                self._stop_requested = False
                
                time.sleep(DT)
                
                if not self._stop_requested:
                    return event_value
                return None
            
            except Exception as e:
                logging.error("Error in E_DELAY: %s", str(e))
                return None

        elif event_name == 'STOP':
            self._stop_requested = True
            return None
    
    def __del__(self):
        logging.info('E_DELAY class destroyed')