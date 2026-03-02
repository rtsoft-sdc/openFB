class STEST_END:
    def schedule(self, event_name, event_value):
        if event_name == 'REQ':
            pass
        return tuple()

    def __del__(self):
        print('class destroyed')
