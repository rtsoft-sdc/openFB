class E_R_TRIG:
    def __init__(self):
        self.last = False

    def schedule(self, event_name, event_value, QI):
        if event_name == 'EI':
            if QI and not self.last:
                self.last = QI
                return event_value, None
            self.last = QI