import logging
class E_DEMUX_8:
    def schedule(self, event_name, event_value, K):
        if event_name == 'EI' and K in range(2):
            try:
                return tuple(event_value if i == K else None for i in range(2))
    
            except Exception as e:
                logging.error("Error in E_DEMUX_8: %s", str(e))
                return None
    def __del__(self):
        logging.info('E_DEMUX_8 class destroyed')