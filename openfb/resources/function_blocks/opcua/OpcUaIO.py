class OpcUaIO:
    def __init__(self):
        self.channel = None
        self.browse_path = None
        self.QO = False
        self.status = "Created"
        self.updated = False

    def bind_channel(self, channel):
        self.channel = channel

    def _init_block(self, QI, PARAMS):
        if not QI:
            self.QO = False
            self.status = "Disabled"
            return False

        self.browse_path = str(PARAMS).strip().strip("'\"") if PARAMS else None
        if not self.browse_path:
            self.QO = False
            self.status = "Invalid PARAMS: BrowsePath missing"
            return False

        self.QO = True
        self.status = "OK"
        return True

    def _check_ready(self, QI):
        if not QI or not self.channel:
            self.QO = False
            self.status = "Not Ready"
            return False
        return True

    def exec_io(self, func, *args, **kwargs):
        return func(*args, **kwargs)