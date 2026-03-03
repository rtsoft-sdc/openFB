import logging
class E_CTUD:
    def __init__(self):
        self.CV = 0
        self.QU = False
        self.QD = False

    def schedule(self, event_name, event_value, PV=None):
        if event_name == 'CU':
            try:
                self.CV += 1
                self.QU = (self.CV >= PV) if PV is not None else False
                self.QD = (self.CV == 0)
                return event_value, self.QU, self.CV, self.QD
            except Exception as e:
                logging.error("Error in E_CTUD: %s", str(e))
                return event_value, None

        elif event_name == 'CD':
            if self.CV > 0:
                self.CV -= 1
            self.QU = (self.CV >= PV) if PV is not None else False
            self.QD = (self.CV == 0)
            return event_value, self.QU, self.CV, self.QD
        elif event_name == 'R':
            self.CV = 0
            self.QU = (self.CV >= PV) if PV is not None else False
            self.QD = (self.CV == 0)
            return event_value, self.QU, self.CV, self.QD
        elif event_name == 'LD':
            if PV is not None:
                self.CV = PV
            self.QU = (self.CV >= PV) if PV is not None else False
            self.QD = (self.CV == 0)
            return event_value, self.QU, self.QD, self.CV
        return None
    
    def __del__(self):
        logging.info('E_CTUD class destroyed')