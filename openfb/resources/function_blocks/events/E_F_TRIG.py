class E_F_TRIG:
    def __init__(self):
        self.last = False

    def schedule(self, event_name, event_value, QI):
        if event_name == 'EI':
            if not QI and self.last:
                self.last = QI
                return event_value
            self.last = QI