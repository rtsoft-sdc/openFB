import logging
class E_TRIG:
  
    def __init__(self, resource=None):
        self.resource = resource
    
    def schedule(self, event_name, event_value, EVENTTYPE):
        if event_name == 'REQ':
            try:
                if self.resource and hasattr(self.resource, 'trigger_events_by_type'):
                    self.resource.trigger_events_by_type(EVENTTYPE)
                return event_value
        
            except Exception as e:
                logging.error("Error in E_TRIG: %s", str(e))
                return None
    def __del__(self):
        logging.info('E_TRIG class destroyed')