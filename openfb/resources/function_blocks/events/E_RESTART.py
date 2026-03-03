import logging
class E_RESTART:
    """Service block for resource restart events"""
    def __init__(self):
        self._restart_type = None

    def schedule(self, event_name, event_value=None):
        pass

    def __del__(self):
        logging.info('E_RESTART class destroyed')