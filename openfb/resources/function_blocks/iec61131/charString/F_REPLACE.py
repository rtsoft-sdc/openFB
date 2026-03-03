import logging
class F_REPLACE:
    def schedule(self, event_name, event_value, IN1, IN2, L, P):
        if event_name == 'REQ':
            s = '' if IN1 is None else str(IN1)
            rep = '' if IN2 is None else str(IN2)
            try:
                l = int(L)
            except Exception as e:
                l = 0
                logging.error("Error in F_REPLACE: Invalid length L: %s", str(L))
            try:
                p = int(P)
            except Exception as e:
                p = 1
                logging.error("Error in F_REPLACE: Invalid position P: %s", str(P))
            idx = max(0, p - 1)
            before = s[:idx]
            after = s[idx + max(0, l):]
            return event_value, before + rep + after

    def __del__(self):
        logging.info('F_REPLACE class destroyed')
