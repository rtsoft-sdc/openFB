class E_DEMUX_8:
    def schedule(self, event_name, event_value, K):
        if event_name == 'EI' and K in range(2):
            return tuple(event_value if i == K else None for i in range(2))