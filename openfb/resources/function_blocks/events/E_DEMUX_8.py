import logging
class E_DEMUX_8:
    def schedule(self, event_name, event_value, K):
        if event_name == 'EI' and K in range(8):
            try:
                return tuple(event_value if i == K else None for i in range(8))
            except Exception as e:
                logging.error("Error in E_DEMUX_8: %s", str(e))
                return None