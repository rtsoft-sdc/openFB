import logging
class F_MID:
    def schedule(self, event_name, event_value, IN, L, P):
        if event_name == 'REQ':
            s = '' if IN is None else str(IN)
            try:
                l = int(L)
            except Exception as e:
                l = 0
                logging.error("Error in F_MID: Invalid length L: %s", str(L))
            try:
                p = int(P)
            except Exception as e:
                p = 1
                logging.error("Error in F_MID: Invalid position P: %s", str(P))
            start = max(0, p - 1)
            if l <= 0:
                return event_value, ''
            return event_value, s[start:start + l]

    def __del__(self):
        logging.info('F_MID class destroyed')
