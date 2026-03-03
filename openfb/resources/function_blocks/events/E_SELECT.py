import logging
class E_SELECT:
    def schedule(self, event_name, event_value, G):
        if event_name == 'EI0' and not G:
            try:
                return event_value
            except Exception as e:
                logging.error("Error in E_SELECT: %s", str(e))
                return None

        elif event_name == 'EI1' and G:
            return event_value
        return None
    
    def __del__(self):
        logging.info('E_SELECT class destroyed')