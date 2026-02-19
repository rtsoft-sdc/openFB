class E_CYCLE:
    import time

    def __init__(self):
        self.running = False

    def schedule(self, event_name, event_value, DT):
        if event_name == 'START':
            self.running = True
            results = []
            while self.running:
                results.append(event_value)
                if isinstance(DT, (int, float)) and DT > 0:
                    self.time.sleep(DT)
                else:
                    break
            return results
        elif event_name == 'STOP':
            self.running = False
            return None
        return None