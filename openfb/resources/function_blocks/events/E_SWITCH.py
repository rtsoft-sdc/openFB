import logging
class E_SWITCH:
    def schedule(self, event_name, event_value, G):
        if event_name == 'EI':
            try:
                if not G:
                    return event_value, None
                else:
                    return None, event_value    
            except Exception as e:
                logging.error("Error in E_SWITCH: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('E_SWITCH class destroyed')