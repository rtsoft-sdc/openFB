import datetime

class F_NOW:
    def schedule(self, event_name, event_value):
        if event_name == 'REQ':
            current_datetime = datetime.datetime.now()
            return event_value, current_datetime

    def __del__(self):
        print('class destroyed')
