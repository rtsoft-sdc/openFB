import time

class OUT_ANY_CONSOLE:
    def schedule(self, event_name, event_value, QI, LABEL, IN):
        # if event_name == 'INIT':
        #     event_name = 'REQ'
        if event_name == 'REQ' and QI == True:
            print(f"T#{time.time()}\tINFO: {LABEL}: {IN}")
            return event_value, 1
