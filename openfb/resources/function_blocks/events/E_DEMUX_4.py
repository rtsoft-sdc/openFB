import logging
class E_DEMUX_4:
    def schedule(self, event_name, event_value, K):
        if event_name == 'EI' and K in range(4):
            try:
                return tuple(event_value if i == K else None for i in range(4))
    
            except Exception as e:
                logging.error("Error in E_DEMUX_4: %s", str(e))
                return None
    def __del__(self):
        logging.info('E_DEMUX_4 class destroyed')