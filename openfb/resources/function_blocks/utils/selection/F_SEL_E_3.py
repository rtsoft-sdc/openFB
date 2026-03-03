import logging


class F_SEL_E_3:
    def schedule(self, event_name, event_value, IN1, IN2, IN3):
        if event_name == 'REQ1':
            return event_value, IN1
        elif event_name == 'REQ2':
            return event_value, IN2
        elif event_name == 'REQ3':
            return event_value, IN3

    def __del__(self):
        logging.info('class destroyed')
