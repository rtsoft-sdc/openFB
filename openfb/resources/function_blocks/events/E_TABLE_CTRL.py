class E_TABLE_CTRL:
    def __init__(self):
        self.CV = 0
        self.DTO = None
        self.DT = [None] * 4

    def schedule(self, event_name, event_value, DT=None, N=None):
        if event_name == 'INIT':
            if DT is not None:
                self.DT = DT if isinstance(DT, list) else [DT]
            if N is not None and N > 0:
                self.CV = 0
                self.DTO = self.DT[0] if len(self.DT) > 0 else None
                return event_value, self.DTO, self.CV
            return event_value, None, 0
        elif event_name == 'CLK':
            if self.CV < 3 and N is not None and self.CV < (N - 1):
                self.CV += 1
                self.DTO = self.DT[self.CV] if self.CV < len(self.DT) else None
                return event_value, self.DTO, self.CV

