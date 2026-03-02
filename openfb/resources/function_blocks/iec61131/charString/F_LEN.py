class F_LEN:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            return event_value, len(IN)
 

    def __del__(self):
        print('F_LEN class destroyed')
