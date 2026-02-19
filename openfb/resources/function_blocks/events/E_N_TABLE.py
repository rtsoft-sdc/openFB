class E_N_TABLE:
    def schedule(self, event_name, event_value, DT, N):
        if event_name == 'START':
            return [event_value for _ in range(min(N, 4))] #need2remake
        elif event_name == 'STOP':
            return None