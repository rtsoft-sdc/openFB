class E_CTUD_UDINT:
    def __init__(self):
        self.CV = 0
        self.QU = False
        self.QD = False

    def schedule(self, event_name, event_value, PV=None):
        if event_name == 'CU':
            self.CV += 1
        elif event_name == 'CD':
            if self.CV > 0:
                self.CV -= 1
        elif event_name == 'R':
            self.CV = 0
        elif event_name == 'LD' and PV is not None:
            self.CV = PV
        self.QU = (self.CV >= PV) if PV is not None else False
        self.QD = (self.CV == 0)
        if event_name == 'CU' or event_name == 'CD':
            return event_value, self.QU, self.CV, self.QD
        elif event_name == 'R':
            return event_value, self.QU, self.CV, self.QD
        elif event_name == 'LD':
            return event_value, self.QU, self.QD, self.CV
        return None