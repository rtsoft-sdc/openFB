import logging

class EMB_RES:
    def __del__(self):
        # cleanup logic
        logging.debug("Object is being destroyed")

    def schedule(self):
        return [1, 0, 0]

